from django.db import models


class User(models.Model):
	uid = models.IntegerField(primary_key=True)
	first_name = models.CharField(max_length=50)
	access_token = models.CharField(max_length=255)

	def __unicode__(self):
		return self.first_name