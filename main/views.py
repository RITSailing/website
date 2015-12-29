from django.shortcuts import render
from social.exceptions import AuthForbidden
from django.shortcuts import render
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.http import HttpResponseRedirect

def auth_allowed(backend, details, response, *args, **kwargs):
    email = details.get('email')
    if email:
        domain = email.split('@', 1)[1]
        if domain is 'g.rit.edu':
            if User.objects.get(email=email):
                raise render(response, 'main/register.html', {'unauthrized': True, 'email': email, 'first': details.get('first_name'), 'last': details.get('last_name')})
            else:
                raise render(response, 'main/rit_student.html')

def home(request):
    return render(request, 'main/home.html')

def events(request):
    return render(request, 'main/events.html')

def files(request):
    return render(request, 'main/files.html')

def members(request):
    return render(request, 'main/members.html')

def register(request):
    return render(request, 'main/register.html')
