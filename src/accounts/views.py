from .serializers import UserSerializer
from .models import User
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import redirect
from .Globals import KAKAO_CONFIG, kakao_login_uri ,kakao_token_uri, kakao_profile_uri
import requests
from django import utils
from uuid import uuid4
import json

class UserList(generics.ListAPIView):
  queryset = User.objects.all()
  serializer_class = UserSerializer

class KakaoLogin(APIView):
  def get(self, request):
    client_id = KAKAO_CONFIG['KAKAO_REST_API_KEY']
    redirect_uri = "http://127.0.0.1:8000/users/kakao-oauth/" # TODO 이거 너무 하드 코딩

    uri = f"{kakao_login_uri}?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
    
    res = redirect(uri)
    return res

class UserInfoFromKakao(APIView) :
  def get(self, request, format=None) :
    data = request.query_params.copy()

    code = data.get('code')
    if not code :
      return Response(status=status.HTTP_400_BAD_REQUEST)
    
    payload = (
      "grant_type=authorization_code&"
      "client_id=" + KAKAO_CONFIG["KAKAO_REST_API_KEY"] + "&"
      "code=" + code + "&"
      "redirect_uri=" + request.build_absolute_uri().split('?')[0]
    )

    headers = {
      'Content-Type': 'application/x-www-form-urlencoded'
    }

    token_response = requests.post(kakao_token_uri, headers=headers, data=payload)
    token = token_response.json().get('access_token')

    headers = {
      'Authorization': 'Bearer ' + token,
      'Content-type': 'application/x-www-form-urlencoded;charset=utf-8'
    }

    user_info_response = requests.get(kakao_profile_uri, headers=headers)
    user_info = user_info_response.json()

    id_from_kakao = user_info.get('id')
    nickname_from_kakao = user_info.get('properties').get('nickname')
    img_from_kakao = user_info.get('properties').get('thumbnail_image')
    
    try :
      new_user = User.objects.get(id=id_from_kakao)
      new_user.nickname = nickname_from_kakao
      new_user.profile_img = img_from_kakao
      new_user.updated_at = utils.timezone.now()
      new_user.user_token = uuid4()
      response = Response(status=status.HTTP_200_OK)
    except User.DoesNotExist :
      new_user = User.objects.create(id=id_from_kakao, nickname=nickname_from_kakao, profile_img=img_from_kakao, create_at=utils.timezone.now(), updated_at=utils.timezone.now(), user_token=uuid4())
      response = Response(status=status.HTTP_201_CREATED)
    new_user.save()

    serializer = UserSerializer(new_user)
    response.data = serializer.data
    return response