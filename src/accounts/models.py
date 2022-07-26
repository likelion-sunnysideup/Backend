from django.db import models

class User(models.Model):
  id = models.IntegerField(primary_key=True)
  nickname = models.CharField(max_length=30, null=False, blank=False, unique=True)
  profile_img = models.URLField(null=False, blank=False)
  create_at = models.DateTimeField(null=False, blank=False)
  updated_at = models.DateTimeField(null=False, blank=False)
  user_token = models.CharField(max_length=30, null=False, blank=False, unique=True)
