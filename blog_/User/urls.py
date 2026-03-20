from django.urls import path
from User.API.user import Register,Login
from User.API.blog import CreatePost,UpdatePost,DeletePost
from User.API.comment import AddComment,ReplyComment,PostComments,LikePost,DeleteComment
from User.API.dashboard import viewDashboard,EditProfile,Home

urlpatterns = [
    path("api/user/register", Register.as_view(), name="register"),
    path("api/user/login", Login.as_view(), name="login"),
    path("api/post/create",CreatePost.as_view(),name="Create post"),
    path("api/post/update/<int:post_id>",UpdatePost.as_view(),name="Update post"),
    path("api/post/delete/<int:post_id>",DeletePost.as_view(),name="delete_post"),
    path("api/comment/add/<int:post_id>",AddComment.as_view(),name="add comment"),
    path("api/comment/reply/<int:comment_id>",ReplyComment.as_view(),name="reply_comment"),
    path("api/post/<int:post_id>/comment",PostComments.as_view(),name="post_comment_view"),
    path("api/post/like/<int:post_id>",LikePost.as_view(),name="like_post"),
    path("api/comment/delete/<int:comment_id>",DeleteComment.as_view(),name="delete comment"),
    path("api/dashboard",viewDashboard.as_view(),name="view_dashboard"),
    path("api/dashboard/edit",EditProfile.as_view(),name="edit profile"),
    path("api/Home",Home.as_view(),name="home")]