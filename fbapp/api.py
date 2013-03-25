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
		if User.objects.get(uid=uid):
			v = Video(vid=vid, uri=uri, user=User.objects.get(uid=uid))
			v.save()
			response.update({'response': '1'})
		else:
			response.update({'response': '0'})
	except Exception:
		response.update({'response': '0'})
	return HttpResponse(simplejson.dumps(response), content_type='application/json')
