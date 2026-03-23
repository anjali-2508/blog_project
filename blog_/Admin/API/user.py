from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from Admin.serializer import AdminUserSerializer
from User.models import UserDetails


#Get all user
class GetUser(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        try:
            if request.user.userdetails.role != 'admin':
                return Response({"status":"fail","message":"only admin can access"})
            user=User.objects.all()
            if not user.exists():
                return Response({
                    "status":"fail",
                    "message":"users not found"
                })
            serializer=AdminUserSerializer(user,many=True)
            return Response({
                "status":"success",
                "data":serializer.data
            })
        except Exception as e:
            return Response({
                "status":"error","message":f"internal server error {str(e)}"
            })
            
#delete user
class Deleteuser(APIView):
    permission_classes=[IsAuthenticated]
    def delete(self,request,user_id):
        try:
            if request.user.userdetails.role != 'admin':
                return Response({"status":"fail","message":"only admin can access"})
            user=User.objects.filter(id=user_id).first()
            if not user:
                return Response({
                    "status":"fail",
                    "message":"user not found"
                })
            user.delete()
            return Response({"status":"success","message":"user deleted successfully"})
        except Exception as e:
            return Response({"status":"error","message":f"internal server error {str(e)}"})

