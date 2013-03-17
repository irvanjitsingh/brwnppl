from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'fbapp.auth.authenticate'),
    url(r'^form/', 'fbapp.home.home'),
    url(r'^oauth/', 'fbapp.auth.oauth'),
    url(r'^record/', 'fbapp.auth.oauth'),
)
