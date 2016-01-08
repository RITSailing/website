from django.shortcuts import render, get_object_or_404
from main.models import TeamMember
from .models import Post
from el_pagination.decorators import page_template
from django.conf import settings

@page_template('blog/post_page.html')
def main(request, template='blog/post_page_index.html', extra_context=None):
	member = None
	if request.user.is_authenticated() and TeamMember.objects.filter(user=request.user).first():
		member = TeamMember.objects.get(user=request.user)
	posts = Post.objects.all()
	version = settings.VERSION
	context = {
		'version':version,
		'page_template':page_template,
		'posts':posts,
		'member':member
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
