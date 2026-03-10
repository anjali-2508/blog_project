from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    author=serializers.CharField(source='user.username')
    class Meta:
        model = Post
        fields = ['id','title','content','author']
        
    
