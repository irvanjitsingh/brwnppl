from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.context_processors import csrf
from fbapp.models import User, Video
import requests, urlparse, random, pdb


def home(request):
	if request.session.get('uid'):
		name = User.objects.get(uid=request.session.get('uid')).first_name
		videos = Video.objects.all()
	c = RequestContext(request, {'uid': request.session['uid'], 'videos':videos})
	return render_to_response('home.html', c)


def upload(request):
	if request.session.get('uid'):
		uid = request.session['uid']
	c = RequestContext(request, {'uid': uid)
	return render_to_response('upload.html', c)