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
		uid = request.session['uid']
	c = RequestContext(request, {'uid': uid, 'videos':videos})
	return render_to_response('home.html', c)


def watch(request, vid):
	if request.session.get('uid'):
		uid = request.session['uid']
		video = Video.objects.get(vid=vid)
	c = RequestContext(request, {'uid': uid, 'video':video})
	return render_to_response('watch.html', c)


def upload(request):
	if request.session.get('uid'):
		uid = request.session['uid']
	c = RequestContext(request, {'uid': uid})
	return render_to_response('upload.html', c)


def vote(request):
	response = {}
	if request.method == 'POST':
		try:
			video = Video.objects.get(vid=vid)
		except Exception:
			response.update({'response': 'failed'})
			return HttpResponse(response)
		if request.POST['type'] == 'up':
			video.upvotes = video.upvotes + 1
		else:
			video.upvotes = video.upvotes - 1
		video.save()


# def rate(request, vid, rating):
# 	if request.session.get('uid'):
# 		video = User.objects.get(vid=vid)
# 	c = RequestContext(request, {'uid': request.user, 'video':video})
# 	return render_to_response('watch.html', c)


def profile(request):
	if request.session.get('uid'):
		user = User.objects.get(uid=request.session['uid'])
		context = {'user':user}
		if request.POST == ['edit']:
			context['edit'] = edit
	c = RequestContext(request, context)
	return render_to_response('profile.html', c)




