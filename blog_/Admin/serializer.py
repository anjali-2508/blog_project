from rest_framework import serializers
from django.contrib.auth.models import User
from User.models import Category,Post,Like,Comment

class AdminUserSerializer(serializers.ModelSerializer):
    role=serializers.CharField(source='userdetails.role')
    created_at = serializers.DateTimeField(source='userdetails.created_at', read_only=True)
    class Meta:
        model=User
        fields=['id','username','email','created_at','role']
        
class AdminCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=['category_id','category_name']

class AdminPostSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(source='created_by.username')
    likes=serializers.IntegerField(source='likes.count')
    comments = serializers.IntegerField(source='comments.count')
    class Meta:
        model=Post
        fields=['post_id','title','created_by','likes','comments']

class AdminCommentSerializer(serializers.ModelSerializer):
    commet_by=serializers.CharField(source='comment_by.username')
    post_title = serializers.CharField(source='post.title')
    replies = serializers.SerializerMethodField()
    class Meta:
        model=Comment
        fields=['comment_id','post_title','comment_by','comment_text','replies']
    def get_replies(self, obj):
        children = Comment.objects.filter(parent_comment=obj)
        return AdminCommentSerializer(children, many=True).data