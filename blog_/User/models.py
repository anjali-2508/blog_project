from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class UserDetails(models.Model):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('user', 'User'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    bio = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "user_details"
        
class Category(models.Model):
    category_id= models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=50)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "category"

    def __str__(self):
        return self.category_name
class Tag(models.Model):
    tag_id = models.AutoField(primary_key=True)
    tag_name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "tag"

    def __str__(self):
        return self.tag_name



class Post(models.Model):
    post_status=(('draft','Draft'),
                 ('published','Published'))
    post_id = models.AutoField(primary_key=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,null=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    tag=models.ManyToManyField(Tag,through='PostTag')
    post_image = models.ImageField(upload_to='images/',blank=True,null=True)
    post_link=models.URLField(null=True,blank=True)
    status= models.CharField(max_length=10,choices=post_status,default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "post"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_by = models.ForeignKey(User, on_delete=models.CASCADE)
    parent_comment=models.ForeignKey('self',on_delete=models.CASCADE,null=True,blank=True)
    comment_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "comment"
        ordering = ["-created_at"]
        
class Like(models.Model):
    like_id=models.AutoField(primary_key=True)
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    liked_by=models.ForeignKey(User,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table='likes'
        unique_together=('post','liked_by')

        
class JWTToken(models.Model):
    token_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "jwt_token"
        
class PostView(models.Model):
    view_id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "post_view"
        

class PostTag(models.Model):
    post_tag_id = models.AutoField(primary_key=True)
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    tag=models.ForeignKey(Tag,on_delete=models.CASCADE)
    class Meta:
        db_table='post_tag'
        unique_together=('post', 'tag')