from .models import Post, Whether
from rest_framework import serializers
from accounts.serializers import UserSerializer

class PostSerializers(serializers.ModelSerializer) :
  class Meta :
    model = Post
    fields = ['id', 'title', 'img_url', 'visibility', 'longitude', 'latitude', 'start_time', 'end_time', 'whether_approved', 'whether', 'writer', 'top', 'pants', 'shoes', 'tips']
    extra_kwargs = {'whether': {'required': False}}
  
  def to_representation(self, instance):
    self.fields['writer'] = UserSerializer(read_only=True)
    self.fields['whether'] = WhetherRepresentationSerializer(read_only=True)
    return super(PostSerializers, self).to_representation(instance)

class WhetherSerializers(serializers.ModelSerializer) :
  class Meta :
      model = Whether
      fields = ['post', 'temperature_max', 'temperature_min', 'temperature_avg', 'precipitation_avg', 'wind_speed_avg', 'humidity_avg']

  def to_representation(self, instance):
    self.fields['post'] = PostSerializers(read_only=True)
    return super(WhetherSerializers, self).to_representation(instance)

class WhetherRepresentationSerializer(serializers.ModelSerializer) :
    class Meta :
      model = Whether
      fields = ['temperature_max', 'temperature_min', 'temperature_avg', 'precipitation_avg', 'wind_speed_avg', 'humidity_avg']

class PostRequestSerializers(serializers.Serializer) :
  whether = WhetherRepresentationSerializer()
  writer_id = serializers.IntegerField()
  title = serializers.CharField(max_length=50)
  img_url = serializers.URLField()
  visibility = serializers.CharField(max_length=10)
  longitude = serializers.FloatField()
  latitude = serializers.FloatField()
  start_time = serializers.DateTimeField()
  end_time = serializers.DateTimeField()
  whether_approved = serializers.BooleanField()
  top = serializers.CharField(max_length=200)
  pants = serializers.CharField(max_length=200)
  shoes = serializers.CharField(max_length=200)
  tips = serializers.CharField(max_length=300)