from django.shortcuts import render, get_object_or_404
from main.models import TeamMember
from .models import Post
from flatpages.models import FlatPage
from el_pagination.decorators import page_template
from django.conf import settings
from events.models import Event

@page_template('blog/post_page.html')
def main(request, template='blog/post_list.html', extra_context=None):
	member = None
	if request.user.is_authenticated() and TeamMember.objects.filter(user=request.user).first():
		member = TeamMember.objects.get(user=request.user)

	version = settings.VERSION
	carousel = Post.objects.exclude(header_image__exact='').order_by('-date')[:3]
	posts = Post.objects.exclude(pk__in=carousel)
	items = list(posts.exclude(pinned_post=True)) + list(Event.objects.all())
	sorted_items = list(Post.objects.filter(pinned_post=True).order_by('-date')) + sorted(items, key=lambda x: x.date, reverse=True)
	context = {
		'version':version,
		'page_template':page_template,
		'carousel':carousel,
		'items':sorted_items,
		'member':member,
		'flatpages':FlatPage.objects.all(),
	}
	if extra_context is not None:
		context.update(extra_context)
	return render(request, template, context)

def post(request, pk, template='blog/full_post_page.html'):
	member = None
	if request.user.is_authenticated() and TeamMember.objects.filter(user=request.user).first():
		member = TeamMember.objects.get(user=request.user)
	post = get_object_or_404(Post, pk=pk)
	version = settings.VERSION
	return render(request, template, {'version':version, 'post': post, 'member': member})
