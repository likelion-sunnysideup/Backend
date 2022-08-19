from csv import unregister_dialect
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
  photo = serializers.ImageField(use_url=True)

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
    fields = ['id', 'title', 'photo', 'visibility', 'longitude', 'latitude', 'start_time', 'end_time', 'whether_approved', 'whether', 'writer', 'top', 'pants', 'shoes', 'tips']
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

class PostRequestSerializers(serializers.ModelSerializer) :
  photo = serializers.ImageField(use_url=True)

  class Meta:
    model = Post
    fields = ['whether','title','photo','visibility','longitude','latitude','start_time','end_time','whether_approved','top','pants','shoes','tips']