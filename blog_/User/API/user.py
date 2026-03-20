from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from User.models import UserDetails
import re
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from datetime import timedelta
from User.models import JWTToken


# user registretion
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
                return Response({"status": "fail", "message": "username already exist"})

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
            UserDetails.objects.create(user=user)
            return Response(
                {"status": "success", "message": "user register successfully"}
            )
        except Exception as e:
            return Response(
                {"status": "error", "message": f"internal server error {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# user login
class Login(APIView):
    def post(self,request):
        try:
            username=request.data.get("username")
            password = request.data.get("password")
            if not username or not password:
                return Response(
                    {"status":"fail","message": "username and password required"})
            user = authenticate(request,username=username, password=password)
            if user is None:
                return Response(
                    {"status":"fail","message": "Invalid username or password"} )
            JWTToken.objects.filter(user=user, is_active=True).update(is_active=False)
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            expiry = timezone.now() + timedelta(hours=1)
            JWTToken.objects.create(
                user=user,
                token=access_token,
                expires_at=expiry,
                is_active=True
            )
            return Response(
                {
                "status":"success",
                "message": "Login successful",
                "data":{
                    "user_id":user.id,
                    "username":user.username,
                    "email": user.email,
                    "token": access_token
                },
            })
        except Exception as e:
            return Response(
                 {"status": "error", "message": f"internal server error {str(e)}"},
                 status=status.HTTP_500_INTERNAL_SERVER_ERROR)        
            