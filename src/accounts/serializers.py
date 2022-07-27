from .models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['id', 'nickname', 'profile_img', 'create_at', 'updated_at', 'user_token']