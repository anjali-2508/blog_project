from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(source='created_by.username')
    category=serializers.CharField(source='category.name',allow_null=True)
    class Meta:
        model = Post
        fields = ['id','title','category','content','created_by']