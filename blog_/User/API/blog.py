from rest_framework.views import APIView
from rest_framework.response import Response
from User.models import Post
from rest_framework.permissions import IsAuthenticated
from User.models import Category

class CreatePost(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        try:
            title = request.data.get("title")
            content = request.data.get("content")
            status_value = request.data.get("status", "draft")
            post_image = request.FILES.get("post_image")
            post_link = request.data.get("post_link")
            category_id = request.data.get("category")
            if not title or not content:
                return Response({
                    "status": "fail",
                    "message": "title and content required"
                }, status=400)
            if status_value not in ["draft", "published"]:
                return Response({
                    "status": "fail",
                    "message": "Invalid status"
                }, status=400)
                
            category = None
            if category_id:
                try:
                    category = Category.objects.get(category_id=category_id)
                except Category.DoesNotExist:
                    return Response({
                        "status": "fail",
                        "message": "Invalid category"
                    }, status=400)
            post = Post.objects.create(
                created_by=request.user,
                title=title,
                content=content,
                status=status_value,
                post_image=post_image,
                post_link=post_link,
                category=category
            )

            return Response({
                "status": "success",
                "message": "post created",
                "data": {
                    "id": post.post_id,
                    "user":request.user.username,
                    "title": post.title,
                    "content": post.content,
                    "status":post.status,
                    "post_image":post.post_image.url if post.post_image else None,
                    "post_link":post.post_link,
                    "category": category.category_name if category else None
    
                }
            })

        except Exception as e:
            return Response({
                "status": "error",
                "message": f"internal server error {str(e)}"}, status=500)
            
#update own post
class UpdatePost(APIView):
    permission_classes =[IsAuthenticated]
    def put(self,request,post_id):
        try:
            post=Post.objects.get(post_id=post_id)
            if post.created_by == request.user:
                title = request.data.get("title")
                content = request.data.get("content")
                if title is not None and title.strip() != "":
                    post.title = title

                if content is not None and content.strip() != "":
                    post.content = content

                post.save()

                return Response({
                    "status": "success",
                    "message": "post updated successfully"
                })

            else:
                return Response({
                    "status": "fail",
                    "message": "Not allowed"
                }, status=403)

        except Post.DoesNotExist:
            return Response({
                "status": "fail",
                "message": "Post not found"
            }, status=404)

        except Exception as e:
            return Response({
                "status": "error",
                "message": str(e)}, status=500)
            
#Delete Post
class DeletePost(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self,request,post_id):
        try:
            post=Post.objects.get(post_id=post_id)
            if post.created_by == request.user:
                post.delete()
                return Response({
                    "status":"success","message":"post deleted successully"
                })
            else:
                return Response({"status":"fail","message":"you can delete only your post"})
        except Exception as e:
            return Response({"status":"error","message":f"internal server error {str(e)}"})
        

