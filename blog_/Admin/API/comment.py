from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from User.models import Comment
from Admin.serializer import AdminCommentSerializer

class ViewComments(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        try:
            if request.user.userdetails.role != 'admin':
                return Response({"status":"fail","message":"only admin can access"},status=401)
            comments = Comment.objects.filter(parent_comment=None)
            if not comments.exists():
                return Response({"status": "fail", "message": "no comments found"},status=404)
            serializer = AdminCommentSerializer(comments, many=True)
            return Response({"status": "success", "data": serializer.data})
        except Exception as e:
            return Response({"status":"error","message":f"internal server error {str(e)}"},status=500)
        
class DeleteComment(APIView):
    permission_classes=[IsAuthenticated]
    def delete(self,request,comment_id):
        try:
            if request.user.userdetails.role != 'admin':
                    return Response({"status":"fail","message":"only admin can access"},status=401)
            comment = Comment.objects.filter(comment_id=comment_id).first()
            if not comment:
                return Response({"status":"fail","message":"comment not found"},status=404)
            comment.delete()
            return Response({"status":"success","message":"comment deleted successfully"})
        except Exception as e:
            return Response({"status":"error","message":f"internal server error {str(e)}"},status=500)

     