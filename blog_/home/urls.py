from django.urls import path
from . import views

urlpatterns = [
    path("api/user/register", views.Register.as_view(), name="register"),
    path("api/user/login", views.login.as_view(), name="login"),
    path("api/post/create", views.CreatePost.as_view(), name="create_post"),
    path("api/post/update/<int:post_id>",views.UpdatePost.as_view(),name="update_post"),    
    path("api/post/delete/<int:post_id>",views.Deletepost.as_view(),name="delete_post"),
    path("api/post/list",views.Viewpost.as_view(),name="view_post"),
    path("api/comment/add",views.Addcomment.as_view(),name="add comment")
]