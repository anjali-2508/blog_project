from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .serializer import PostSerializer
from .models import Post, Comment, Category
import re
from rest_framework.permissions import AllowAny

# Create your views here.


# registration
class Register(APIView):
    def post(self, request):
        try:
            username = request.data.get("username")
            email = request.data.get("email")
            password = request.data.get("password")
            if not username or not email or not password:
                return Response(
                    {
                        "status": "fail",
                        "message": "username,email and password required",
                    }
                )
            email_validation = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,7}"
            if not re.fullmatch(email_validation, email):
                return Response({"status": "fail", "message": "enter valid email"})
            if User.objects.filter(email=email).exists():
                return Response({"status": "fail", "message": "email already exist"})
            if User.objects.filter(username=username).exists():
                return Response({"status":"fail","message":"username already exist"})
            
            if len(password) < 8:
                return Response(
                    {
                        "status": "fail",
                        "message": "password must be at least 8 character long",
                    }
                )
            
            user = User.objects.create_user(
                username=username, email=email, password=password
            )
            return Response(
                {"status": "success", "message": "user register successfully"}
            )
        except Exception as e:
            return Response(
                {"status": "error", "message": f"internal server error {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# login
class login(APIView):
    def post(self, request):
        try:
            username = request.data.get("username")
            password = request.data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                refresh = RefreshToken.for_user(user)
                return Response(
                    {
                        "status": "success",
                        "message": "Login successful",
                        "data": {
                            "user_id": user.id,
                            "username": user.username,
                            "email": user.email,
                            "token": str(refresh.access_token),
                        },
                    }
                )
            else:
                return Response(
                    {"status": "fail", "message": "Invalid username or password"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Exception as e:
            return Response(
                {"status": "error", "message": f"internal server error {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# create post
class CreatePost(APIView):
    def post(self, request):
        try:
            if not request.user.is_authenticated:
                return Response(
                    {
                        "status": "fail",
                        "message": "Authentication required to create a post",
                    },
                    status=status.HTTP_401_UNAUTHORIZED,
                )
            image = request.FILES.get("image")
            title = request.data.get("title")
            content = request.data.get("content")
            category = request.data.get("category")
            if not title or not content or not category:
                return Response(
                    {"status": "fail", "message": "title, content, and category cannot be empty"}
                )
            category,created = Category.objects.get_or_create(name=category)
            post = Post.objects.create(created_by=request.user, title=title, content=content, category=category,image=image)
            return Response(
                {
                    "status": "success",
                    "message": "Blog post created successfully",
                    "data": {
                        "post_id": post.id,
                        "post_title": post.title,
                        "post_content": post.content,
                        "category": post.category.name,
                        "created_by": post.created_by.username,
                    },
                }
            )
        except Exception as e:
            return Response(
                {"status": "error", "message": f"internal server error {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# update post
class UpdatePost(APIView):
    def put(self, request, post_id):
        try:
            if request.user.is_authenticated:
                post = Post.objects.get(id=post_id)
                if post.created_by == request.user:
                    title = request.data.get("title")
                    content = request.data.get("content")
                    if title is not None and title != "":
                        post.title = title
                    if content is not None and content != "":
                        post.content = content
                    post.save()
                    return Response(
                        {
                            "status": "success",
                            "message": "Blog post updated successfully",
                        }
                    )

                else:
                    return Response(
                        {
                            "status": "fail",
                            "message": "You can edit only your own post",
                        },
                        status=status.HTTP_401_UNAUTHORIZED,
                    )
            else:
                return Response(
                    {
                        "status": "fail",
                        "message": "authentication require to update post",
                    },
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        except Exception as e:
            return Response(
                {"status": "error", "message": f"internal server error {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# delete post
class Deletepost(APIView):
    def delete(self, request, post_id):
        try:
            if request.user.is_authenticated:
                post = Post.objects.get(id=post_id)
                if post.created_by == request.user:
                    post.delete()
                    return Response(
                        {"status": "success", "message": "post deleted successfully"}
                    )
                else:
                    return Response(
                        {
                            "status": "fail",
                            "message": "You can only delete your own post",
                        },
                        status=status.HTTP_401_UNAUTHORIZED,
                    )
        except Exception as e:
            return Response(
                {"status": "error", "message": f"internal server error {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# view all post
class Viewpost(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        try:
            post = Post.objects.all()
            serializer = PostSerializer(post, many=True)
            return Response(
                {
                    "status": "success",
                    "message": "post retrived successfully",
                    "data": serializer.data,
                }
            )
        except Exception as e:
            return Response(
                {"status": "error", "message": f"internal sever error {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# add comment
class Addcomment(APIView):
    def post(self, request):
        try:
            post_id = request.data.get("post_id")
            comment = request.data.get("comment")
            if request.user.is_authenticated:
                if not post_id or not comment:
                    return Response(
                        {
                            "status": "fail",
                            "message": "post id or comment cannot be empty",
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                else:
                    post = Post.objects.get(id=post_id)
                    Comment.objects.create(
                        user=request.user, post=post, comment=comment
                    )
                    return Response(
                        {"status": "success", "message": "comment added successfully"}
                    )
            else:
                return Response(
                    {
                        "status": "fail",
                        "message": "authentication required to add comment",
                    },
                    status=status.HTTP_401_UNAUTHORIZED,
                )

        except Exception as e:
            return Response(
                {"status": "error", "message": f"internal server error {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class Categorywisepost(APIView):
    permission_classes = [AllowAny]
    def get(self, request, category_name):
        try:
            category = Category.objects.get(name=category_name)
            posts = Post.objects.filter(category=category)
            serializer = PostSerializer(posts, many=True)
            return Response(
                {
                    "status": "success",
                    "message": "posts retrived successfully",
                    "data": serializer.data,
                }
            )
        except Category.DoesNotExist:
            return Response(
                {"status": "fail", "message": "category not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response(
                {"status": "error", "message": f"internal server error {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )