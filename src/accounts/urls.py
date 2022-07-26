from django.urls import path, include
from . import views
from rest_framework import urls

urlpatterns =[
  path('', views.UserList.as_view()),
  path('kakao-login/', views.KakaoLogin.as_view()),
  path('kakao-oauth/', views.UserInfoFromKakao.as_view())
]