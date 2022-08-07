from rest_framework import viewsets, generics, mixins, views
from .models import Post, Whether
from accounts.models import User
from rest_framework import status
from .serializers import PostSerializers, WhetherSerializers, PostRequestSerializers
from rest_framework.response import Response
from django.db.models import Q
import json

# Create your views here.
class PostListView( 
  mixins.ListModelMixin, 
  generics.GenericAPIView
) :
  queryset = Post.objects.all()
  serializer_class = PostSerializers

  def get(self, request, *args, **kwargs) :
    if 'user-id' in request.GET :
      data = Post.objects.filter(writer=request.GET['user-id'])
      post_serializer = PostSerializers(data, many=True)
      return Response(post_serializer.data, status=status.HTTP_200_OK)
    else :
      return self.list(request, *args, **kwargs)
  
  def post(self, request, *args, **kwargs):
    request_serializer = PostRequestSerializers(data=request.data)
    if not request_serializer.is_valid() :
      return Response(request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    print(request_serializer.data)
    request_body = request_serializer.data

    new_post = {
      'writer' : request_body.get('writer_id'),
      'title' : request_body.get('title'),
      'img_url' : request_body.get('img_url'),
      'visibility' : request_body.get('visibility'),
      'longitude' : request_body.get('longitude'),
      'latitude' : request_body.get('latitude'), 
      'start_time' : request_body.get('start_time'), 
      'end_time' : request_body.get('end_time'),
      'whether_approved' : request_body.get('whether_approved'),
      'top' :  request_body.get('top'),
      'pants' : request_body.get('pants'),
      'shoes' : request_body.get('shoes'),
      'tips' : request_body.get('tips')
    }
    
    post_serializer = PostSerializers(data=new_post)
    if not post_serializer.is_valid():
      return Response(post_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    post_serializer.save()
    
    whether_info = request_body.get('whether')
    new_wheter = {
      'post' : post_serializer.data.get('id'),
      'temperature_max' : whether_info.get('temperature_max'),
      'temperature_min' : whether_info.get('temperature_min'),
      'temperature_avg' : whether_info.get('temperature_avg'),
      'precipitation_avg' : whether_info.get('precipitation_avg'),
      'wind_speed_avg' : whether_info.get('wind_speed_avg'),
      'humidity_avg' : whether_info.get('humidity_avg')
    }
    whetherSerializers = WhetherSerializers(data=new_wheter)
    if not whetherSerializers.is_valid():
      return Response(whetherSerializers.errors, status=status.HTTP_400_BAD_REQUEST)
    whetherSerializers.save()

    new_post = Post.objects.get(id=post_serializer.data.get('id'))
    new_post = {
      'writer' : new_post.writer.id,
      'whether' : new_post.id,
      'title' : new_post.title,
      'img_url' : new_post.img_url,
      'visibility' : new_post.visibility,
      'longitude' : new_post.longitude,
      'latitude' : new_post.latitude, 
      'start_time' : new_post.start_time, 
      'end_time' : new_post.end_time,
      'whether_approved' : new_post.whether_approved,
      'top' :  new_post.top,
      'pants' : new_post.pants,
      'shoes' : new_post.shoes,
      'tips' : new_post.tips
    }
    post_serializer = PostSerializers(data=new_post)
    if not post_serializer.is_valid():
      return Response(post_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(post_serializer.data, status=status.HTTP_201_CREATED)

class PostListByWhetherView( 
  mixins.ListModelMixin, 
  generics.GenericAPIView
) :
  queryset = Post.objects.all()
  serializer_class = PostSerializers

  def get(self, request, *args, **kwargs) :
    temp_avg_tolerance = 3.0
    temp_avg_min = 4
    temp_avg_max = 27.0

    wind_speed_tolerance = 2.0
    wind_speed_min = 2.0
    wind_speed_max = 8.0

    temp_avg = float(request.GET["temp-avg"])
    precipitation = float(request.GET["precipitation"])
    wind_speed = float(request.GET["wind-speed"])

    if temp_avg < temp_avg_min :
      temp_avg_query = Q(whether__temperature_avg__lte=temp_avg_min)
    elif temp_avg > temp_avg_max :
      temp_avg_query = Q(whether__temperature_avg__gte=temp_avg_max)
    else :
      temp_avg_range = (temp_avg - temp_avg_tolerance, temp_avg + temp_avg_tolerance)
      temp_avg_query = Q(whether__temperature_avg__range=temp_avg_range)

    if precipitation == 0.0 :
      precipitation_query = Q(whether__precipitation_avg__lt=0.2)
    elif precipitation < 2.5 :
      precipitation_query = Q(whether__precipitation_avg__range=(0.2, 3.0))
    elif precipitation < 15 : 
      precipitation_query = Q(whether__precipitation_avg__range=(2.0, 15.0))
    else :
      precipitation_query = Q(whether__precipitation_avg__gte=15.0)

    if wind_speed < wind_speed_min :
      wind_speed_query = Q(whether__wind_speed_avg__lte=wind_speed_min)
    elif wind_speed > wind_speed_max :
      wind_speed_query = Q(whether__wind_speed_avg__gte=wind_speed_max)
    else :
      wind_speed_range = (wind_speed - wind_speed_tolerance, wind_speed + wind_speed_tolerance)
      wind_speed_query = Q(whether__wind_speed_avg__range=wind_speed_range)
    
    queryset = (
      Post.objects
        .filter(temp_avg_query)
        .filter(precipitation_query)
        .filter(wind_speed_query)
    )

    page = self.paginate_queryset(queryset)
    if page is not None:
      serializer = self.get_serializer(page, many=True)
      return self.get_paginated_response(serializer.data)

    serializer = self.get_serializer(queryset, many=True)
    return Response(serializer.data)


class PostDetailView(generics.RetrieveUpdateDestroyAPIView) :
  queryset = Post.objects.all()
  serializer_class = PostSerializers

class WhetherViewSet(viewsets.ModelViewSet) :
  queryset = Whether.objects.all()
  serializer_class = WhetherSerializers

whetherList = WhetherViewSet.as_view({
  'get' : 'list',
  'post' : 'create',
})