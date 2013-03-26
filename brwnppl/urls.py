from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^admin/', include(admin.site.urls)),

	#auth
	url(r'^login/$', 'fbapp.auth.authenticate'),
	url(r'^oauth/$', 'fbapp.auth.oauth'),


	url(r'^$', 'fbapp.core.home'),
	url(r'^upload/$', 'fbapp.core.upload'),
	url(r'^profile/$', 'fbapp.core.profile'),
	
	#playback
	url(r'^watch/(?P<vid>\d+)/?$', 'fbapp.core.watch'),

	#video interaction
	url(r'^vote/?$', 'fbapp.core.vote'),
	url(r'^vote/(?P<vid>\d+)/(?P<direction>.+)/?$', 'fbapp.core.vote'),
	url(r'^rate/(?P<vid>\d+)/(?P<rating>\d+)/?$', 'fbapp.core.rate'),

	#api
	url(r'^api/1/videos/add/$', 'fbapp.api.create'),
	# url(r'^api/1/videos/delete/(?P<vid>\d+)/(?P<uid>\d+)/?$', 'fbapp.api.create'),
	# url(r'^api/1/videos/add/(?P<vid>\d+)/(?P<uid>\d+)/?$', 'fbapp.api.create'),
)
