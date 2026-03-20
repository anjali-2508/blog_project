from django.urls import path
from Admin.API.user import GetUser,Deleteuser
from Admin.API.category import Addcategory,EditCategory,DeleteCategory,Viewcategory
from Admin.API.post import ViewPost,DeletePost

urlpatterns = [
    path("api/admin/user", GetUser.as_view(), name="Get all user"),
    path("api/admin/user/<int:user_id>",Deleteuser.as_view,name="delete user"),
    path("api/admin/category",Addcategory.as_view(),name='add category'),
    path("api/admin/category/<int:category_id",EditCategory.as_view(),name='edit category'),
    path("api/admin/category/<int:category_id>",DeleteCategory.as_view(),name='delete category'),
    path("api/admin/category",Viewcategory.as_view(),name='view all category'),
    path("api/admin/posts",ViewPost.as_view(),name="view posts"),
    path("api/admin/post/<int:post_id>",DeletePost.as_view(),name="delete post")]