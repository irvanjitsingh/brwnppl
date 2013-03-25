from fbapp.models import User, Video
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json as simplejson

@csrf_exempt
def create(request):
	response={}
	try: 
		data = simplejson.loads(request.raw_post_data)
		vid=data["vid"]
		uri=data["uri"]
		uid=data["uid"]
		test = [uid, vid]
		try:
			if User.objects.get(uid=uid):
				try:
					v = Video(vid=vid, uri=uri, user=User.objects.get(uid=uid))
					v.save()
					response.update({'response': 'success'})
				except Exception:
					response.update({'response':'failed to save'})
			else:
				response.update({'response': 'user does not exist'})
		except Exception:
			response.update({'response': 'failed to identify'})
	except Exception:
		response.update({'response': 'json error'})
	return HttpResponse(simplejson.dumps(response), content_type='application/json')
