from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register(r'', views.WhetherViewSet,basename="whether/")

urlpatterns =[
  path('', views.PostListView.as_view()),
  path('<int:pk>/', views.PostDetailView.as_view()),
  path('by-whether', views.PostListByWhetherView.as_view()),
  path('whether/', views.whetherList)
]