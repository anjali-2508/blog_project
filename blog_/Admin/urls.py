from django.urls import path
from Admin.API.user import GetUser,Deleteuser
from Admin.API.category import Addcategory,EditCategory,DeleteCategory,Viewcategory
from Admin.API.post import ViewPost,DeletePost
from Admin.API.comment import ViewComments,DeleteComment

urlpatterns = [
    path("api/admin/user/view", GetUser.as_view(), name="Get all user"),
    path("api/admin/user/delete/<int:user_id>",Deleteuser.as_view(),name="delete user"),
    path("api/admin/category",Addcategory.as_view(),name='add category'),
    path("api/admin/category/edit/<int:category_id>",EditCategory.as_view(),name='edit category'),
    path("api/admin/category/delete/<int:category_id>",DeleteCategory.as_view(),name='delete category'),
    path("api/admin/category/view",Viewcategory.as_view(),name='view all category'),
    path("api/admin/posts",ViewPost.as_view(),name="view posts"),
    path("api/admin/post/<int:post_id>",DeletePost.as_view(),name="delete post"),
    path("api/admin/comment",ViewComments.as_view(),name="view comment"),
    path("api/admin/comment/<int:comment_id>",DeleteComment.as_view(),name="delete comment")
    ]