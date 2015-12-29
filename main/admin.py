from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
# from main.models import TeamMember
from django import forms

# class UsersChangeForm(UserChangeForm):
#     class Meta(UserChangeForm.Meta):
#         model = TeamMember
#
# class UsersAdmin(UserAdmin):
#     form = UsersChangeForm
#
#     fieldsets = UserAdmin.fieldsets + (
#             (None, {'fields': ('college',)}),
#     )
#
#
# admin.site.register(TeamMember, UsersAdmin)
