from django.conf.urls import patterns, include, url
from django.contrib.auth.views import logout
from main import views

urlpatterns = [
    url(r'^members/$', views.page, {"template":"main/members.html"}),
    url(r'^members/search/$', views.search_members),
    url(r'^members/(?P<username>[a-zA-Z ].*)/edit/$', views.edit_profile, name="edit"),
    url(r'^members/(?P<username>[a-zA-Z ].*)/$', views.profile, name="member"),
    url(r'^register/success/$', views.page, {"template":"main/success.html"}),
    url(r'^register/$', views.register, name="register"),
    url(r'^logout/$', logout),
]
