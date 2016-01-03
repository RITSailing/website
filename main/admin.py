from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from main.models import TeamMember, Request
from django import forms

class TeamMemberAdmin(admin.ModelAdmin):
	list_display = ('name', 'year_level', 'sailing_level', 'is_dues_paid')
	search_fields = ('user',)

	def name(self, instance):
		return instance.user.first_name + " " + instance.user.last_name
	name.short_description = "Name"

	def is_dues_paid(self, instance):
		return instance.is_dues_paid()
	is_dues_paid.short_description = "Dues Paid?"

	def get_form(self, request, obj=None, **kwargs):
		self.exclude = []
		if not request.user.is_staff:
			self.exclude.append('eboard_pos')
		return super(TeamMemberAdmin, self).get_form(request, obj, **kwargs)

class RequestAdmin(admin.ModelAdmin):
	list_display = ('email', 'name', 'year_level', 'accepted')
	list_editable = ('accepted',)
	list_filter = ('accepted',)
	search_fields = ('email', 'first_name', 'last_name')

	def name(self, instance):
		return instance.first_name + " " + instance.last_name
	name.short_description = "Name"

admin.site.register(TeamMember, TeamMemberAdmin)

admin.site.register(Request, RequestAdmin)
