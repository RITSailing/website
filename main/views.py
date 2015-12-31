from social.exceptions import AuthForbidden
from django.shortcuts import render, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from social.pipeline.user import USER_FIELDS
from models import TeamMember, Request
from responseutils import HttpRedirectException
from forms import RegisterForm
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
		fill_member_info(kwargs['response']['image'], member[0], details.get('email'))
		return {'is_new': False}

	fields = dict((name, kwargs.get(name) or details.get(name))
				  for name in strategy.setting('USER_FIELDS',
											   USER_FIELDS))
	if not fields:
		return

	user = strategy.create_user(**fields)
	member = TeamMember.objects.get_or_create(user=user)
	fill_member_info(kwargs['response']['image'], member[0], details.get('email'))

	return {
		'is_new': True,
		'user': user
	}

def fill_member_info(image, member, email):
	member.avatar = image['url'].split('?')[0]
	# Delete the Request of the user that is being moved to member
	if Request.objects.filter(email=email).first():
		request = Request.objects.get(email=email)
		member.year_level = request.year_level
		request.delete()
	member.save()
	send_conformation_email(email)

def send_conformation_email(email):
	# TODO send the person a conformation email telling them that they signed up
	placeholder = None

def page(request, template):
	member = None
	if request.user.is_authenticated() and TeamMember.objects.filter(user=request.user).first():
		member = TeamMember.objects.get(user=request.user)
	return render(request, template, {'member':member})

def profile(request, username):
	user = get_object_or_404(User, username=username)
	view_member = get_object_or_404(TeamMember, user=user)
	member = None
	if request.user.is_authenticated() and TeamMember.objects.filter(user=request.user).first():
		member = TeamMember.objects.get(user=request.user)
	return render(request, "main/profile.html", {'member':member, 'view_member': view_member})

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
