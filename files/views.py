from django.shortcuts import render, get_object_or_404
from .models import Folder, File
from main.models import TeamMember

def files(request, template):
	children_folders = Folder.objects.filter(parent=None)
	children_files = File.objects.filter(parent=None)
	Member = None
	if request.user.is_authenticated() and TeamMember.objects.filter(user=request.user).first():
		member = TeamMember.objects.get(user=request.user)

	return render(request, template, {'files':children_files, 'folders':children_folders, 'member':member})

def folder(request, path):
	path_items = path.split('/')
	end = path_items[len(path_items)-1]
	if len(path_items) < 2:
		parent_file = get_object_or_404(Folder, parent=None, name__iexact=end)
	else:
		parent = path_items[len(path_items)-2]
		parent_file = get_object_or_404(Folder, parent=Folder.objects.filter(name__iexact=parent), name__iexact=end)
	children_folders = Folder.objects.filter(parent=parent_file)
	children_files = File.objects.filter(parent=parent_file)
	path_urls = []
	temp = '/files'
	for item in path_items:
		temp += ("/" + item)
		path_urls.append({'name': Folder.objects.get(name__iexact=item).name, "url": str(temp).lower()})
	Member = None
	if request.user.is_authenticated() and TeamMember.objects.filter(user=request.user).first():
		member = TeamMember.objects.get(user=request.user)

	return render(request, 'main/files.html', {'path':path_urls, 'files':children_files, 'folders':children_folders, 'member':member})
