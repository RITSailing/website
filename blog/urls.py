from django.conf.urls import patterns, include, url
from blog import views

urlpatterns = [
    url(r'^$', views.main),
    url(r'^blog/post/(?P<pk>\w+)$', views.post, name='post'),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
]
