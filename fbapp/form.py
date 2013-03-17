from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.context_processors import csrf
from fbapp.models import User
import requests, urlparse, random, pdb


def form(request):
	if request.session.get('uid'):
		name = User.objects.get(uid=request.session.get('uid')).first_name
	c = RequestContext(request, {'name': name})
	return render_to_response('form.html', c)