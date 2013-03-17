from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt

def view(request):
	text = 'Hello World!'
	c = RequestContext(request, {'content': text})
	return render_to_response('app.html', c)