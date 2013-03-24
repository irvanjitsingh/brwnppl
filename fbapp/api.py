from fbapp.models import User, Video
from django.http import HttpResponse


def create(request, uid, vid, uri):
	if User.objects.get(uid=uid):
		v = Video(vid=vid, user=User.objects.get(uid=uid))
		v.save()
		response = uri
		test = "t"
	else:
		response = 0
	return HttpResponse(response)
