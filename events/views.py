from django.shortcuts import render,  get_object_or_404, get_list_or_404
from django.http import HttpResponseRedirect
from .models import Event
from main.models import TeamMember
from django.conf import settings

def events(request, template):
	events = Event.objects.all()
	member = None
	if request.user.is_authenticated() and TeamMember.objects.filter(user=request.user).first():
		member = TeamMember.objects.get(user=request.user)
	version = settings.VERSION
	return render(request, template, {'version':version, 'events':events, 'member':member})

def rsvp(request, pk):
    next = request.GET.get('next', None)
    event = get_object_or_404(Event, pk=pk)
    member = get_object_or_404(TeamMember, user=request.user)
    if member in event.going.all():
        return render(request, "events/error.html", {'message':"You've already RSVP'ed to this event."})
    else:
        event.going.add(member)
        event.save()
    if next:
        return HttpResponseRedirect(next)
    else:
        return HttpResponseRedirect('/events/')

def un_rsvp(request, pk):
    next = request.GET.get('next', None)
    event = get_object_or_404(Event, pk=pk)
    member = get_object_or_404(TeamMember, user=request.user)
    if member not in event.going.all():
        return render(request, "events/error.html", {'message':"You've haven't RSVP'ed to this event yet."})
    else:
        event.going.remove(member)
        event.save()
    if next:
        return HttpResponseRedirect(next)
    else:
        return HttpResponseRedirect('/events/')
