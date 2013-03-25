from fbapp.models import User, Video
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json as simplejson, pdb

@csrf_exempt
def create(request):
	response={}
	try: 
		data = simplejson.loads(request.raw_post_data)
		vid=int(data["vid"])
		uri=data["uri"]
		uid=int(data["uid"])
		print request.raw_post_data
		print vid
		print uid
		print uri
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
