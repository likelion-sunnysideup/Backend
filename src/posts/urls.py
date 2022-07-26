from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register(r'', views.PostViewSet,basename="")
router.register(r'', views.WhetherViewSet,basename="whether/")

urlpatterns =[
  path('', views.postList),
  path('whether/', views.whetherList)
]