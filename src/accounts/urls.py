from django.urls import path, include
from . import views
from rest_framework import urls
from .views import UserViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'dev-users', UserViewSet, basename='dev-users')

urlpatterns =[
  path('', views.UserList.as_view()),
  path('kakao-login/', views.KakaoLogin.as_view()),
  path('kakao-oauth/', views.UserInfoFromKakao.as_view()),
  path('auth/',views.GetByToken.as_view()),
]
urlpatterns += router.urls