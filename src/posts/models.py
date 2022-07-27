from django.db import models

# Create your models here.
class Post(models.Model) :
  id = models.AutoField(primary_key=True)
  writer = models.ForeignKey("accounts.User", related_name="post", on_delete=models.CASCADE, db_column="writer_id")
  title =  models.CharField(max_length=50, null=False, blank=False)
  img_url =  models.URLField(null=False, blank=False)
  top =  models.CharField(max_length=200, null=False, blank=False)
  pants =  models.CharField(max_length=200, null=False, blank=False)
  shoes =  models.CharField(max_length=200, null=False, blank=False)
  tips =  models.CharField(max_length=300, null=False, blank=False)

class Whether(models.Model) :
  post = models.OneToOneField("Post", related_name="whether", on_delete=models.CASCADE, db_column="post_id", primary_key=True)
  temperature_max = models.FloatField(null=True, blank=True)
  temperature_min = models.FloatField(null=True, blank=True)
  temperature_avg = models.FloatField(null=True, blank=True)
  precipitation_avg = models.FloatField(null=True, blank=True)
  wind_speed_avg = models.FloatField(null=True, blank=True)
  humidity_avg = models.FloatField(null=True, blank=True)