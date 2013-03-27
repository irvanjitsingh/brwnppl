from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.core.context_processors import csrf
from django.contrib.auth.models import User
from fbapp.models import User
import requests, urlparse, random, pdb

app_id = '222454974560719'
app_secret = '18e694d08042bd899c01411369493ffd'
redirect_uri = 'https://bpbhangra.herokuapp.com/oauth/'
permissions = 'publish_stream'


@csrf_exempt
def authenticate(request):
	request.session['state'] = random.getrandbits(128)
	dialog_redirect = (
		'https://www.facebook.com/dialog/oauth?client_id=%(id)s&redirect_uri=%(uri)s&scope=%(permissions)s&state=%(state)s'
		% {'id': app_id, 'uri': redirect_uri, 'permissions':permissions, 'state': request.session.get('state') })
	return HttpResponseRedirect(dialog_redirect)

def oauth(request):
	if request.session.get('state') and (request.session.get('state') == int(request.REQUEST['state'])):
		code = request.REQUEST['code']
		app_info = {'client_id': app_id, 'redirect_uri': redirect_uri, 'client_secret': app_secret, 'code': code}
		token_request = requests.get('https://graph.facebook.com/oauth/access_token', params=app_info)
		response = token_request.text
		access_token = urlparse.parse_qs(response)['access_token'][0]
		info = requests.get('https://graph.facebook.com/me', params={'access_token': access_token}).json()
		uid = info['id']
		name = info['first_name']
		request.session['uid'] = uid
		request.session['name'] = uid
		if not User.objects.filter(uid=uid):
			user = User(uid=uid, first_name=name, access_token=access_token)
			user.save()
		return HttpResponseRedirect('/home')
	else:
		text = 'Error: CSRF token could not be validated.'
		c = RequestContext(request, {'content': text})
		return render_to_response('app.html', c)





