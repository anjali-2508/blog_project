from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from User.models import Post,Comment,Like
from rest_framework.response import Response
from User.serializer import CommentSerializer


class AddComment(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        try:
            post = Post.objects.get(post_id=post_id)

            comment_text = request.data.get("comment_text")

            if not comment_text or comment_text.strip() == "":
                return Response({
                    "status": "fail",
                    "message": "Comment cannot be empty"}, status=400)

            comment = Comment.objects.create(
                post=post,
                comment_by=request.user,
                comment_text=comment_text.strip()
            )

            return Response({
                "status": "success","message": "comment added"})

        except Post.DoesNotExist:
            return Response({"status": "fail","message": "Post not found"}, status=404)
        
#reply comment
class ReplyComment(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, comment_id):
        try:
            parent_comment = Comment.objects.get(comment_id=comment_id)

            reply_text = request.data.get("comment_text")
            if not reply_text or reply_text.strip() == "":
                return Response({
                    "status": "fail",
                    "message": "Reply cannot be empty"
                }, status=400)

            # create reply
            reply = Comment.objects.create(
                post=parent_comment.post,
                comment_by=request.user,
                comment_text=reply_text.strip(),
                parent_comment=parent_comment
            )

            return Response({
                "status": "success",
                "message": "reply added",
                "data": {
                    "comment_id": reply.comment_id,
                    "post_id": parent_comment.post.post_id,
                    "user": request.user.username,
                    "comment_text": reply.comment_text,
                    "parent_comment": parent_comment.comment_id
                }
            })

        except Exception as e:
            return Response({
                "status": "error",
                "message": f"internal server error {str(e)}"
            }, status=500)
            
#view comments for a post
class PostComments(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, post_id):
        comments = Comment.objects.filter(post_id=post_id)
        serializer = CommentSerializer(comments, many=True)
        return Response({
            "status": "success",
            "comments": serializer.data})

#delete comment
class DeleteComment(APIView):
    permission_classes=[IsAuthenticated]
    def delete(self,request,comment_id):
        try:
            comment = Comment.objects.get(comment_id=comment_id)
            if comment.comment_by==request.user or comment.post.created_by==request.user:
                comment.delete()
                return Response({"status":"success","message":"comment deleted successfully"})
            return Response({"status":"fail",
                            "message":"you can delete only you comment"})
        except Comment.DoesNotExist:
            return Response({"status":"fail","message":"comment does not exits"})
        except Exception as e:
            return Response({
                "status":"error",
                "message":f"internal server error {str(e)}"},status=500)
        
#like post
class LikePost(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        try:
            post = Post.objects.get(post_id=post_id)
            if Like.objects.filter(post=post,liked_by=request.user).exists():
                return Response({"status":"fail","message":"already like"})
            like, created = Like.objects.get_or_create(post=post, liked_by=request.user)
            total_likes=Like.objects.filter(post=post).count()
            return Response({"status":"success","message":"Post liked",
                             "data":{
                                 "post_id":post.post_id,
                                 "total_likes":total_likes
                             }})
        except Post.DoesNotExist:
            return Response({"status":"fail","message":"post not found"},status=400)
        except Exception as e:
            return Response({"status":"error","message":f"internal server error {str(e)}"})
            
        
       