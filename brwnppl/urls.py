from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^admin/', include(admin.site.urls)),
	#auth
	url(r'^$', 'fbapp.auth.authenticate'),
	url(r'^oauth/$', 'fbapp.auth.oauth'),
	url(r'^home/$', 'fbapp.core.home'),
	#api
	url(r'^api/1/videos/add/(?P<uid>\d+)/(?P<vid>\d+)/(?P<uri>.+)/?$', 'fbapp.api.create'),
	# url(r'^api/1/videos/delete/(?P<vid>\d+)/(?P<uid>\d+)/?$', 'fbapp.api.create'),
	# url(r'^api/1/videos/add/(?P<vid>\d+)/(?P<uid>\d+)/?$', 'fbapp.api.create'),
)
