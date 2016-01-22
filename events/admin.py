from django.contrib import admin
from django.core.urlresolvers import reverse
from main.models import TeamMember
from .models import Event

class AdminInline(admin.TabularInline):
	model = Event.going.through
	raw_id_fields = ('teammember',)
	readonly_fields = ['name', 'email', 'sailing_level', 'year_level', 'dues_paid']
	extra = 0

	model.teammember.verbose_name = 'Member'

	def name(self, instance):
		url = reverse("admin:main_teammember_change", args=(instance.teammember.pk,))
		return '<a href="%s">%s</a>' % (url, instance.teammember.user.first_name + " " + instance.teammember.user.last_name)
	name.short_description = 'Name'
	name.allow_tags = True

	def email(self, instance):
		return instance.teammember.user.email

	def sailing_level(self, instance):
		return instance.teammember.get_sailing_level_display()

	def year_level(self, instance):
		return instance.teammember.get_year_level_display()

	def dues_paid(self, instance):
		return instance.teammember.is_dues_paid()
	model._meta.verbose_name_plural = "Members"

class EventAdmin(admin.ModelAdmin):
	inlines = [AdminInline]
	exclude = ('going',)
	list_display = ('title', 'date', 'end_date', 'closed_rsvp',)
	list_filter = ('closed_rsvp',)
	search_fields = ('name','date', 'end_date', )

admin.site.register(Event, EventAdmin)
