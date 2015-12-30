from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from main.models import TeamMember, Request
from django import forms

class TeamMemberAdmin(admin.ModelAdmin):
	def get_form(self, request, obj=None, **kwargs):
		self.exclude = []
		if not request.user.is_staff:
			self.exclude.append('eboard_pos')
		return super(TeamMemberAdmin, self).get_form(request, obj, **kwargs)

admin.site.register(TeamMember, TeamMemberAdmin)

admin.site.register(Request)
