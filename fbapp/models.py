from django.db import models


class User(models.Model):
	uid = models.IntegerField(primary_key=True)
	first_name = models.CharField(max_length=50)
	access_token = models.CharField(max_length=255)

	def __unicode__(self):
		return self.first_name


class Video(models.Model):
	vid = models.BigIntegerField(primary_key=True)
	name = models.CharField(max_length=50)
	user = models.ForeignKey(User)
	uri_v = models.CharField(max_length=300)
	uri_i = models.CharField(max_length=300)
	upvotes = models.IntegerField()
	downvotes = models.IntegerField()
	rating = models.IntegerField()

	def __unicode__(self):
		return self.name