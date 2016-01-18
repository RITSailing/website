from __future__ import unicode_literals
from django.db import models
from main.models import TeamMember

class ItemType(models.Model):
	name = models.CharField(max_length=100)
	descriptor = models.CharField(max_length=3)
	location = models.CharField(max_length=100)
	quantity = models.IntegerField()
	def __str__(self):
		return self.name
	def save(self, **kwargs):
		super(ItemType, self).save(kwargs)
		while Item.objects.filter(item_type=self).count() < self.quantity:
			Item.objects.create_item(self, self.descriptor + "__" + str(Item.objects.filter(item_type=self).count()+1))

class ItemManager(models.Manager):
	def create_item(self, type, id):
		return self.create(item_type=type, descriptor=id)

class Item(models.Model):
	item_type = models.OneToOneField(ItemType)
	descriptor = models.SlugField(default="1")
	notes = models.TextField(blank=True)
	objects = ItemManager()
	def __str__(self):
		return self.descriptor
	def available(self, start_date, end_date):
		request = Request.objects.filter(item_type=self, accepted=True)
		return (min(request.end_date, end_date) - max(request.start_date, start_date)).days + 1 < 0

class Request(models.Model):
	accepted = models.BooleanField(default=False)
	picked_up = models.BooleanField(default=False)
	returned = models.BooleanField(default=False)
	member = models.OneToOneField(TeamMember)
	item = models.ForeignKey(Item)
	start_date = models.DateField()
	end_date = models.DateField()
	notes = models.TextField(blank=True)
	was_checked = models.BooleanField(default=False, editable=False)
	def __str__(self):
		return self.member + ": " + self.item
	def save(self, **kwargs):
		if self.accepted and not self.was_checked:
			d = Context({ 'name': self.member.first_name, })
			text_content = loader.get_template('equipment/accepted_email.txt').render(d)
			html_content = loader.get_template('equipment/accepted_email.html').render(d)
			msg = EmailMultiAlternatives('Equipment Request Accepted', text_content, settings.EMAIL_DEFAULT_FROM, [self.member.email])
			msg.attach_alternative(html_content, "text/html")
			msg.send()
			self.was_checked = True
		elif not self.accepted and self.was_checked:
			# Fired on uncheck if needed later on
			self.was_checked = False
		super(Request, self).save(kwargs)
