from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from User.models import Post
from Admin.serializer import AdminPostSerializer

#view post
class ViewPost(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        try:
            if request.user.userdetails.role != 'admin':
                return Response({"status":"fail","message":"only admin can access"})
            post=Post.objects.all()
            if not post.exists():
                return Response({"status":"fail","message":"posts not found"})
            serializer=AdminPostSerializer(post,many=True)
            return Response({"status":"success","data":serializer.data})
        except Exception as e:
            return Response({"status":"error","message":f"internal server error {str(e)}"},status=500)
        
    
#delete post
class DeletePost(APIView):
    permission_classes=[IsAuthenticated]
    def delete(self,request,post_id):
        try:
            if request.user.userdetails.role != 'admin':
                return Response({"status":"fail","message":"only admin can access"})
            post = Post.objects.filter(post_id=post_id).first()
            if not post:
                return Response({"status":"fail","message":"post not found"})
            post.delete()
            return Response({"status":"success","message":"post deleted successfully"})
        except Exception as e:
            return Response({"status":"error","message":f"internal server error {str(e)}"})
