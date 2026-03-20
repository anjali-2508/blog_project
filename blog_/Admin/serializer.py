from rest_framework import serializers
from django.contrib.auth.models import User
from User.models import Category,Post,Like,Comment

class AdminUserSerializer(serializers.ModelSerializer):
    role=serializers.CharField(source='userdetalis.role')
    class Meta:
        model=User
        fields=['id','username','email','created_at','role']
        
class AdminCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=['category_id','category_name']

class AdminPostSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(source='created_by.username')
    likes=serializers.SerializerMethodField
    comments=serializers.SerializerMethodField
    class Meta:
        model=Post
        fields=['post_id','title','created_by','likes','comments']
    def get_likes(self,obj):
        return Like.objects.filter(post=obj).count()
    def get_comments(self,obj):
        return Comment.objects.filter(post=obj).count()
