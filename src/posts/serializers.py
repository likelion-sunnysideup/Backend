from .models import Post, Whether
from rest_framework import serializers
from accounts.serializers import UserSerializer


class PostSerializers(serializers.ModelSerializer) :
  class Meta :
    model = Post
    fields = ['id', 'whether', 'writer', 'title', 'img_url', 'top', 'pants', 'shoes', 'tips']
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
  top = serializers.CharField(max_length=200)
  pants = serializers.CharField(max_length=200)
  shoes = serializers.CharField(max_length=200)
  tips = serializers.CharField(max_length=300)