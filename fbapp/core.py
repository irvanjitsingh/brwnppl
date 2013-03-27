from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
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
		user = User.objects.get(uid=request.session['uid'])
		uid = user.uid
		video = Video.objects.get(vid=vid)
		upvotes = video.userUpVotes.filter(uid = uid).count()
		downvotes = video.userDownVotes.filter(uid = user.uid).count()
	c = RequestContext(request, {'uid': uid, 'video':video, 'upvotes':upvotes, 'downvotes':downvotes})
	return render_to_response('watch.html', c)


def upload(request):
	if request.session.get('uid'):
		uid = request.session['uid']
	c = RequestContext(request, {'uid': uid})
	return render_to_response('upload.html', c)


def vote(request):
   vid = int(request.POST.get('vid'))
   vote_type = request.POST.get('type')
   vote_action = request.POST.get('action')
   user=User.objects.get(uid=request.session['uid'])
   video = get_object_or_404(Video, pk=vid)

   thisUserUpVote = video.userUpVotes.filter(uid = user.uid).count()
   thisUserDownVote = video.userDownVotes.filter(uid = user.uid).count()

   if (vote_action == 'vote'):
      if (thisUserUpVote == 0) and (thisUserDownVote == 0):
         if (vote_type == 'up'):
            video.userUpVotes.add(user)
         elif (vote_type == 'down'):
            video.userDownVotes.add(user)
         else:
            return HttpResponse('error-unknown vote type')
      else:
         return HttpResponse('error - already voted', thisUserUpVote, thisUserDownVote)
   elif (vote_action == 'recall-vote'):
      if (vote_type == 'up') and (thisUserUpVote == 1):
         video.userUpVotes.remove(user)
      elif (vote_type == 'down') and (thisUserDownVote ==1):
         video.userDownVotes.remove(user)
      else:
         return HttpResponse('error - unknown vote type or no vote to recall')
   else:
      return HttpResponse('error - bad action')


   num_votes = video.userUpVotes.count() - video.userDownVotes.count()

   return HttpResponse(num_votes)


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




