from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from User.models import Post,Comment,Like
from rest_framework.response import Response
from User.serializer import DashboardPostSerializer

class viewDashboard(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user_posts = Post.objects.filter(created_by=request.user)

            if not user_posts.exists():
                return Response({
                    "status": "fail",
                    "message": "No posts found"
                }, status=404)
            serializer=DashboardPostSerializer(user_posts,many=True)
            total_likes=0
            total_comments=0
            for post in user_posts:
                total_likes +=Like.objects.filter(post=post).count()
                total_comments +=Comment.objects.filter(post=post).count()
            return Response({
                "status": "success",
                "data": {
                    "total_posts": user_posts.count(),
                    "total_likes": total_likes,
                    "total_comments": total_comments,
                    "posts":serializer.data
                }
            })

        except Exception as e:
            return Response({
                "status": "error",
                "message": f"Internal server error: {str(e)}"
            }, status=500)
            
class EditProfile(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        try:
            user = request.user

            username = request.data.get("username")
            email = request.data.get("email")
            password = request.data.get("password")
            if not username and not email and not password:
                return Response({
                    "status": "fail",
                    "message": "At least one field is required"
                }, status=400)

            if username:
                user.username = username

            if email:
                user.email = email

            if password:
                user.set_password(password)  

            user.save()

            return Response({
                "status": "success",
                "message": "Profile updated successfully"})

        except Exception as e:
            return Response({
                "status": "error",
                "message": f"Internal server error: {str(e)}"}, status=500)
class Home(APIView):
    def get(self,request):
        try:
            post=Post.objects.all()
            if not post.exists():
                return Response({"status":"fail","message":"post not found"})
            serializer=DashboardPostSerializer(post,many=True)
            return Response({
                "status":"success",
                "data":serializer.data
            })       
        except Exception as e:
            return Response({"status":"error","message":f"internal server error {str(e)}"
            },status=500)
    
