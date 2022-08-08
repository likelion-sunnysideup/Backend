from .models import Post, Whether
from rest_framework import serializers
from accounts.serializers import UserSerializer
import json

class StringListField(serializers.Field) :
  def to_representation(self, value):
    return json.loads(value)

  def to_internal_value(self, data):
    return json.dumps(data)

class PostSerializers(serializers.ModelSerializer) :
  top = StringListField()
  pants = StringListField()
  shoes = StringListField()
  tips = StringListField()

  def get_top(self, obj) :
    return json.loads(obj.top)

  def get_pants(self, obj) :
    return json.loads(obj.pants)

  def get_shoes(self, obj) :
    return json.loads(obj.shoes)

  def get_tips(self, obj) :
    return json.loads(obj.tips)

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
  title = serializers.CharField(max_length=50)
  img_url = serializers.URLField(max_length=500)
  visibility = serializers.CharField(max_length=10)
  longitude = serializers.FloatField()
  latitude = serializers.FloatField()
  start_time = serializers.DateTimeField()
  end_time = serializers.DateTimeField()
  whether_approved = serializers.BooleanField()
  top = StringListField()
  pants = StringListField()
  shoes = StringListField()
  tips = StringListField()