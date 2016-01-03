from social.exceptions import AuthForbidden
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.models import User, Permission
from django.contrib.auth import logout
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect, HttpResponseForbidden
from social.pipeline.user import USER_FIELDS
from .models import TeamMember, Request
from .responseutils import HttpRedirectException
from .forms import RegisterForm, ProfileForm
from events.models import Event
from files.models import File, Folder
# DO NOT TOUCH
# This is a method overide for the auth_allowed step in the social authentication pipline
# It is overrided so that we  can filter who can log in by the people that we have listed
def auth_allowed(backend, details, response, *args, **kwargs):
	email = details.get('email')
	if email:
		domain = email.split('@', 1)[1]
		username = email.split('@', 1)[0]
		if domain == 'g.rit.edu':
			if not User.objects.filter(email=email) and not Request.objects.filter(accepted=True, email=email).first():
				raise HttpRedirectException("register", details)
		else:
			raise AuthForbidden(backend)

# DO NOT TOUCH
# This is a method overide for the create_user step in the social authentication pipline
# It is overrided so that we can create a new TeamMember object to go with the created user
def create_user(strategy, details, user=None, *args, **kwargs):
	if user:
		member = TeamMember.objects.get_or_create(user=user)
		fill_member_info(False, kwargs['response']['image'], member[0], details.get('email'))
		return {'is_new': False}

	fields = dict((name, kwargs.get(name) or details.get(name))
				  for name in strategy.setting('USER_FIELDS',
											   USER_FIELDS))
	if not fields:
		return

	user = strategy.create_user(**fields)
	member = TeamMember.objects.get_or_create(user=user)
	fill_member_info(True, kwargs['response']['image'], member[0], details.get('email'))
	return {
		'is_new': True,
		'user': user
	}

def fill_member_info(new, image, member, email):
	# Set user permissions if the member is staff
	if member.user.is_staff:
		ct = ContentType.objects.get_for_model(TeamMember)
		member.user.user_permissions.add(Permission.objects.get(content_type=ct, codename='change_teammember'))
		ct = ContentType.objects.get_for_model(Request)
		member.user.user_permissions.add(Permission.objects.get(content_type=ct, codename='change_request'))
		ct = ContentType.objects.get_for_model(Event)
		member.user.user_permissions.add(Permission.objects.get(content_type=ct, codename='add_event'))
		member.user.user_permissions.add(Permission.objects.get(content_type=ct, codename='change_event'))
		member.user.user_permissions.add(Permission.objects.get(content_type=ct, codename='delete_event'))
		ct = ContentType.objects.get_for_model(File)
		member.user.user_permissions.add(Permission.objects.get(content_type=ct, codename='add_file'))
		member.user.user_permissions.add(Permission.objects.get(content_type=ct, codename='change_file'))
		member.user.user_permissions.add(Permission.objects.get(content_type=ct, codename='delete_file'))
		ct = ContentType.objects.get_for_model(Folder)
		member.user.user_permissions.add(Permission.objects.get(content_type=ct, codename='add_folder'))
		member.user.user_permissions.add(Permission.objects.get(content_type=ct, codename='change_folder'))
		member.user.user_permissions.add(Permission.objects.get(content_type=ct, codename='delete_folder'))
	else:
		member.user.user_permissions.clear()
	# Set user avatar image
	member.avatar = image['url'].split('?')[0]
	# Delete the Request of the user that is being moved to member
	if Request.objects.filter(email=email).first():
		request = Request.objects.get(email=email)
		member.year_level = request.year_level
		request.delete()
	# Save all of our changes
	member.save()
	member.user.save()
	# Send an email confirming the user creation
	if new:
		send_conformation_email(email)

def send_conformation_email(email):
	# TODO send the person a conformation email telling them that they signed up
	placeholder = None

def page(request, template):
	member = None
	members = TeamMember.objects.all()
	if request.user.is_authenticated() and TeamMember.objects.filter(user=request.user).first():
		member = TeamMember.objects.get(user=request.user)
	return render(request, template, {'members':members, 'member':member})

def profile(request, username):
	user = get_object_or_404(User, username=username)
	view_member = get_object_or_404(TeamMember, user=user)
	member = None
	if request.user.is_authenticated() and TeamMember.objects.filter(user=request.user).first():
		member = TeamMember.objects.get(user=request.user)
	return render(request, "main/profile.html", {'user':user,'member':member, 'view_member': view_member})

def edit_profile(request, username):
	user = get_object_or_404(User, username=username)
	view_member = get_object_or_404(TeamMember, user=user)
	if user is not request.user and not request.user.is_staff:
		raise PermissionDenied
	member = None
	if request.user.is_authenticated() and TeamMember.objects.filter(user=request.user).first():
		member = TeamMember.objects.get(user=request.user)

	data = request.GET
	if request.method == 'POST':
		form = ProfileForm(request.POST, member=member, is_staff=request.user.is_staff)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('member', args=(username,)))
	else:
		form = ProfileForm(member=member, is_staff=request.user.is_staff)
	return render(request, "main/profile.html", {'form':form, 'is_edit': True, 'user':user, 'member':member, 'view_member': view_member})

def register(request):
	data = request.GET
	if request.method == 'POST':
		form = RegisterForm(request.POST, initial=data)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/register/success/')
	else:
		form = RegisterForm(initial=data)
	return render(request, 'main/register.html', {'form':form,})
