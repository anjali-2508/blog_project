from rest_framework import serializers
from User.models import Comment,Post,Like

class CommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = ['comment_id', 'post', 'comment_by', 'comment_text', 'parent_comment', 'created_at','replies']
    def get_replies(self, obj):
        children = Comment.objects.filter(parent_comment=obj)
        return CommentSerializer(children, many=True).data

class DashboardPostSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['post_id', 'title','post_image','post_link', 'likes', 'comments']
    def get_likes(self,obj):
        return Like.objects.filter(post=obj).count()
    def get_comments(self,obj):
        return Comment.objects.filter(post=obj).count()

class HomeSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    created_by=serializers.CharField(source='created_by.username')
    class Meta:
        model = Post
        fields = ['post_id', 'created_by','title','post_image','post_link', 'likes', 'comments']
    def get_likes(self,obj):
        return Like.objects.filter(post=obj).count()
    def get_comments(self,obj):
        return Comment.objects.filter(post=obj).count()