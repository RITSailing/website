"""RITSailing URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.views import logout
from django.conf.urls import include
from django.conf.urls.static import static
from django.conf import settings
from main import views

urlpatterns = [
    url(r'^$', views.page, {"template":"main/base.html"}),
    url(r'^events/$', views.page, {"template":"main/events.html"}),
    url(r'^files/$', views.page, {"template":"main/files.html"}),
    url(r'^members/$', views.page, {"template":"main/members.html"}),
    url(r'^members/(?P<username>[a-zA-Z ].*)/edit/$', views.edit_profile, name="edit"),
    url(r'^members/(?P<username>[a-zA-Z ].*)/$', views.profile, name="member"),
    url(r'^register/success/$', views.page, {"template":"main/success.html"}),
    url(r'^register/$', views.register, name="register"),
    url(r'^logout/$', logout),
	url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^inplaceeditform/', include('inplaceeditform.urls')),
    url(r'^admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
