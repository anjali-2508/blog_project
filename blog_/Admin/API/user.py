from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from Admin.serializer import AdminUserSerializer


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
    def delete(self,request,user_id):
        try:
            if request.user.userdetails.role != 'admin':
                return Response({"status":"fail","message":"only admin can access"})
            user=User.objects.get(id=user_id)
            if not user.exists():
                return Response({
                    "status":"fail",
                    "message":"users not found"
                })
            user.delete()
            return Response({"status":"success","message":"user deleted successfully"})
        except Exception as e:
            return Response({"status":"error","message":f"internal server error {str(e)}"})

