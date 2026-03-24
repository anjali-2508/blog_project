from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from User.models import Category
from Admin.serializer import AdminCategorySerializer

#add category
class Addcategory(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        try:
            if request.user.userdetails.role != 'admin':
                return Response({"status":"fail","message":"only admin can access"},status=401)
            category_name=request.data.get('category_name')
            if not category_name:
                return Response({"status":"fail","message":"category name required"},status=400)
            if Category.objects.filter(category_name=category_name).exists():
                return Response({"status":"fail","message":"category alredy exists"},status=400)
            Category.objects.create(category_name=category_name)
            return Response({"status":"success","message":"category added successfully"})
        except Exception as e:
            return Response({"status":"error","message":f"internal server error {str(e)}"},status=500)

#edit category
class EditCategory(APIView):
    permission_classes=[IsAuthenticated]
    def put(self,request,category_id):
        try:
            if request.user.userdetails.role != 'admin':
                return Response({"status":"fail","message":"only admin can access"},status=401)
            category = Category.objects.filter(category_id=category_id).first()
            
            if not category:
                return Response({"status":"fail","message":"category id not found"},status=404)
            
            category_name=request.data.get('category_name')
            if not category_name:
                return Response({"status":"fail","message":"category name required"},status=400)
            if Category.objects.filter(category_name=category_name).exclude(category_id=category_id).exists():
                return Response({"status":"fail","message":"category name already exists"},status=400)
            category.category_name=category_name
            category.save()
            return Response({"status":"success","message":"category updated successfully"})
        except Exception as e:
            return Response({"status":"error","message":f"internal server error {str(e)}"},status=500)
            
#delete category
class DeleteCategory(APIView):
    permission_classes=[IsAuthenticated]
    def delete(self,request,category_id):
        try:
            if request.user.userdetails.role != 'admin':
                return Response({"status":"fail","message":"only admin can access"},status=401)
            
            category = Category.objects.filter(category_id=category_id).first()
            if not category:
                return Response({"status":"fail","message":"category id not found"},status=404)
            category.delete()
            return Response({"status":"success","message":"category deleted successfully"})
            
        except Exception as e:
            return Response({"status":"error","message":f"internal server error {str(e)}"},status=500)
        
#view category
class Viewcategory(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        try:
            if request.user.userdetails.role != 'admin':
                return Response({"status":"fail","message":"only admin can access"},status=401)
            category=Category.objects.all()
            if not category.exists():
                return Response({"status":"fail","message":"category not found"},status=404)
            serializer=AdminCategorySerializer(category,many=True)
            return Response ({"status":"success",
                              "data":serializer.data})
        except Exception as e:
            return Response({"status":"error","message":f"internal server error {str(e)}"},status=500)