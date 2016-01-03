from django.conf.urls import patterns, include, url
from files import views

urlpatterns = [
    url(r'^files/$', views.files, {"template":"main/files.html"}),
    url(r'^files/(?P<path>[-/\w]+)/$', views.folder, name="folder"),
]
