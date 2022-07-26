from .models import Post, Whether
from rest_framework import serializers
from accounts.serializers import UserSerializer


class PostSerializers(serializers.ModelSerializer) :
  class Meta :
    model = Post
    fields = ['id', 'whether', 'writer', 'title', 'img_url', 'top', 'pants', 'shoes', 'tips']
  
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