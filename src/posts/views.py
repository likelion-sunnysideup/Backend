from rest_framework import viewsets, generics, mixins, views
from .models import Post, Whether
from accounts.models import User
from rest_framework import status
from .serializers import PostSerializers, WhetherSerializers, PostRequestSerializers
from rest_framework.response import Response
from django.db.models import Q
import json

class PostListView(views.APIView) :
  queryset = Post.objects.all()
  serializer_class = PostSerializers
  
  def post(self, request, *args, **kwargs):
    token = request.META.get('HTTP_ACCESSTOKEN')
    try:
      requester = User.objects.get(user_token = token)
    except User.DoesNotExist :
      return Response(status=status.HTTP_401_UNAUTHORIZED)
      
    request_serializer = PostRequestSerializers(data=request.data)
    if not request_serializer.is_valid() :
      return Response(request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    request_body = request_serializer.data

    new_post = {
      'writer' : requester.id,
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
    post_serializer = PostSerializers(new_post)
    return Response(post_serializer.data, status=status.HTTP_201_CREATED)

class PostListByUserView(
  mixins.ListModelMixin, 
  generics.GenericAPIView
) :
  serializer_class = PostSerializers

  def get(self, request, *args, **kwargs) :
    token = request.META.get('HTTP_ACCESSTOKEN')
    try:
      requester = User.objects.get(user_token = token)
    except User.DoesNotExist :
      return Response(status=status.HTTP_401_UNAUTHORIZED)

    if 'user-id' in request.GET :
      self.queryset = Post.objects.filter(writer=request.GET['user-id'])
      return self.list(request, *args, **kwargs)
    else :
      return Response(status=status.HTTP_400_BAD_REQUEST)


class PostListByWhetherView( 
  mixins.ListModelMixin, 
  generics.GenericAPIView
) :
  serializer_class = PostSerializers

  def get(self, request, *args, **kwargs) :
    token = request.META.get('HTTP_ACCESSTOKEN')
    try:
      requester = User.objects.get(user_token = token)
    except User.DoesNotExist :
      return Response(status=status.HTTP_401_UNAUTHORIZED)

    temp_avg_tolerance = 3.0
    temp_avg_min = 4
    temp_avg_max = 27.0

    wind_speed_tolerance = 2.0
    wind_speed_min = 2.0
    wind_speed_max = 8.0

    try :
      temp_avg = float(request.GET["temp-avg"])
      precipitation = float(request.GET["precipitation"])
    except KeyError:
      return Response(status=status.HTTP_400_BAD_REQUEST) 

    wind_speed = float(request.GET.get("wind-speed", "-1.0"))
    humidity = float(request.GET.get("humidity", "-1.0"))

    if temp_avg < temp_avg_min :
      temp_avg_query = Q(whether__temperature_avg__lte=temp_avg_min)
    elif temp_avg > temp_avg_max :
      temp_avg_query = Q(whether__temperature_avg__gte=temp_avg_max)
    else :
      temp_avg_range = (temp_avg - temp_avg_tolerance, temp_avg + temp_avg_tolerance)
      temp_avg_query = Q(whether__temperature_avg__range=temp_avg_range)
    

    if precipitation == 0.0 :
      precipitation_query = Q(whether__precipitation_avg__lt=1.0)
    elif precipitation == 1000.0 :
      precipitation_query = Q(whether__precipitation_avg__gte=0.5)
    elif precipitation < 2.5 :
      precipitation_query = Q(whether__precipitation_avg__range=(0.5, 3.0))
    elif precipitation < 15 : 
      precipitation_query = Q(whether__precipitation_avg__range=(2.0, 15.0))
    else :
      precipitation_query = Q(whether__precipitation_avg__gte=15.0)

    filter_query = temp_avg_query & precipitation_query

    if wind_speed < wind_speed_min :
      wind_speed_query = Q(whether__wind_speed_avg__lte=wind_speed_min)
    elif wind_speed < wind_speed_max :
      wind_speed_range = (wind_speed - wind_speed_tolerance, wind_speed + wind_speed_tolerance)
      wind_speed_query = Q(whether__wind_speed_avg__range=wind_speed_range)
    else :
      wind_speed_query = Q(whether__wind_speed_avg__gte=wind_speed_max)

    if not wind_speed == -1.0 :
      filter_query = filter_query & wind_speed_query
    
    self.queryset = Post.objects.filter(filter_query)

    return self.list(request=request, *args, **kwargs)    

class PostDetailView(generics.RetrieveUpdateDestroyAPIView) :
  queryset = Post.objects.all()
  serializer_class = PostSerializers

  def get(self, request, *args, **kwargs):
    token = request.META.get('HTTP_ACCESSTOKEN')
    try:
      requester = User.objects.get(user_token = token)
    except User.DoesNotExist :
      return Response(status=status.HTTP_401_UNAUTHORIZED)
    return self.retrieve(request, *args, **kwargs)

  def put(self, reques , *args, **kwargs):
    token = request.META.get('HTTP_ACCESSTOKEN')
    try:
      requester = User.objects.get(user_token = token)
    except User.DoesNotExist :
      return Response(status=status.HTTP_401_UNAUTHORIZED)
    return self.update(request, *args, **kwargs)

  def patch(self, request, *args, **kwargs):
    token = request.META.get('HTTP_ACCESSTOKEN')
    try:
      requester = User.objects.get(user_token = token)
    except User.DoesNotExist :
      return Response(status=status.HTTP_401_UNAUTHORIZED)
    return self.partial_update(request, *args, **kwargs)

  def delete(self, request, *args, **kwargs):
    token = request.META.get('HTTP_ACCESSTOKEN')
    try:
      requester = User.objects.get(user_token = token)
    except User.DoesNotExist :
      return Response(status=status.HTTP_401_UNAUTHORIZED)
    return self.destroy(request, *args, **kwargs)

class WhetherViewSet(viewsets.ModelViewSet) :
  queryset = Whether.objects.all()
  serializer_class = WhetherSerializers

whetherList = WhetherViewSet.as_view({
  'get' : 'list',
  'post' : 'create',
})