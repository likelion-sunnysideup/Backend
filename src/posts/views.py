from rest_framework import viewsets
from .models import Post, Whether
from .serializers import PostSerializers, WhetherSerializers
from rest_framework.response import Response

# Create your views here.
class PostViewSet(viewsets.ModelViewSet) :
  queryset = Post.objects.all()
  serializer_class = PostSerializers

  def list(self, request, *args, **kwargs):
    queryset = Post.objects.all()
    serializer = PostSerializers(queryset, many=True)

    print(Post._meta.get_fields())
    print(queryset.first().whether)
    return Response(serializer.data)

postList = PostViewSet.as_view({
  'get' : 'list',
  'post' : 'create',
})

class WhetherViewSet(viewsets.ModelViewSet) :
  queryset = Whether.objects.all()
  serializer_class = WhetherSerializers

whetherList = WhetherViewSet.as_view({
  'get' : 'list',
  'post' : 'create',
})