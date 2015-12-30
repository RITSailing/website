from django.shortcuts import render
from social.exceptions import AuthForbidden
from django.shortcuts import render
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from social.pipeline.social_auth import social_user
from social.exceptions import AuthForbidden
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
# This is a method overide for the associate_user step in the social authentication pipline
# It is overrided so that we can create a new TeamMember object to go with the created user
def associate_user(backend, uid, user=None, social=None, *args, **kwargs):
	member = TeamMember.objects.create_member(user)
	if user and not social:
		try:
			social = backend.strategy.storage.user.create_social_auth(
				user, uid, backend.name
			)
		except Exception as err:
			if not backend.strategy.storage.is_integrity_error(err):
				raise
			# Protect for possible race condition, those bastard with FTL
			# clicking capabilities, check issue #131:
			#   https://github.com/omab/django-social-auth/issues/131
			return social_user(backend, uid, user, *args, **kwargs)
		else:
			return {'social': social,
					'user': social.user,
					'member': member,
					'new_association': True}

# DO NOT TOUCH
# This is a method overide for the user_details step in the social authentication pipline
# It is overrided so that we can fill the new TeamMember object with the information gathered from the login
def user_details(strategy, details, user=None, member=None, *args, **kwargs):
	"""Update user details using data from provider."""
	image = kwargs['response']['image']
	if not member:
		member = TeamMember.objects.get(user=user)
	member.avatar = image['url'].split('?')[0]

	# Delete the Request of the user that is being moved to member
	email = details.get('email')
	if Request.objects.filter(email=email).first():
		request = Request.objects.get(email=email)
		member.year_level = request.year_level
		request.delete()
	member.save()
	send_conformation_email(email)
	if user:
		changed = False  # flag to track changes
		protected = ('username', 'id', 'pk', 'email') + \
			tuple(strategy.setting('PROTECTED_USER_FIELDS', []))

		# Update user model attributes with the new data sent by the current
		# provider. Update on some attributes is disabled by default, for
		# example username and id fields. It's also possible to disable update
		# on fields defined in SOCIAL_AUTH_PROTECTED_FIELDS.
		for name, value in details.items():
			if value and hasattr(user, name):
				# Check https://github.com/omab/python-social-auth/issues/671
				current_value = getattr(user, name, None)
				if not current_value or name not in protected:
					changed |= current_value != value
					setattr(user, name, value)

		if changed:
			strategy.storage.user.changed(user)

def send_conformation_email(email):
	# TODO send the person a conformation email telling them that they signed up
	placeholder

def page(request, template):
	member = None
	if request.user.is_authenticated():
		member = TeamMember.objects.get(user=request.user)
	return render(request, template, {'member':member})

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
