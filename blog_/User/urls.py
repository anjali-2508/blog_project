from django.urls import path
from User.API.user import Register,Login
from User.API.blog import CreatePost,UpdatePost,DeletePost
from User.API.comment import AddComment,ReplyComment,PostComments,LikePost,DeleteComment
from User.API.dashboard import viewDashboard,EditProfile,Home

urlpatterns = [
    #1
    path("api/user/register", Register.as_view(), name="register"),
    #2
    path("api/user/login", Login.as_view(), name="login"),
    #3
    path("api/post/create",CreatePost.as_view(),name="Create post"),
    #4
    path("api/post/update/<int:post_id>",UpdatePost.as_view(),name="Update post"),
    #5
    path("api/post/delete/<int:post_id>",DeletePost.as_view(),name="delete_post"),
    #6
    path("api/comment/add/<int:post_id>",AddComment.as_view(),name="add comment"),
    #7
    path("api/comment/reply/<int:comment_id>",ReplyComment.as_view(),name="reply_comment"),
    #8
    path("api/post/<int:post_id>/comment",PostComments.as_view(),name="post_comment_view"),
    #9
    path("api/post/like/<int:post_id>",LikePost.as_view(),name="like_post"),
    #10
    path("api/comment/delete/<int:comment_id>",DeleteComment.as_view(),name="delete comment"),
    #11
    path("api/dashboard",viewDashboard.as_view(),name="view_dashboard"),
    #12
    path("api/dashboard/edit",EditProfile.as_view(),name="edit profile"),
    #13
    path("api/Home",Home.as_view(),name="home")]
    # path("api/post/list",views.Viewpost.as_view(),name="view_post"),
    # path("api/post/category/<str:category_name>",views.Categorywisepost.as_view(),name="view_post_category")]
