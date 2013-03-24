from fbapp.models import User, Video
from django.http import HttpResponse
import json as simplejson


def create(request):
	response={}
	if User.objects.get(uid=uid):
		try: 
			data = simplejson.loads(request.raw_post_data)
			vid=data["vid"]
			uri=data["uri"]
			uid=data["uid"]
			v = Video(vid=vid, uri=uri, user=User.objects.get(uid=uid))
			v.save()
			response.update({'response': '1'})
		except Exception:
			response.update({'response': '0'})
	else:
		response.update({'response': '0'})
	return HttpResponse(simplejson.dumps(response), content_type='application/json')
