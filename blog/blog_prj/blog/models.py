from django.db import models
from users.models import User
import os
from uuid import uuid4
from django.utils import timezone

# Create your models here.

def upload_filepath(instance, filename):
    today_str=timezone.now().strftime("%Y%m%d") # 현재 시간 가져와서 문자열로 반환환
    file_basename=os.path.basename(filename)
    return f'{instance._meta.model_name}/{today_str}/{str(uuid4)}_{file_basename}'

class Category(models.Model):
    name=models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    title=models.CharField(max_length=50)
    content=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    author=models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="posts")
    category=models.ManyToManyField(to=Category, through="PostCategory", related_name="posts")
    like=models.ManyToManyField(to=User, through="Like", related_name="like_posts")
    image=models.ImageField(upload_to=upload_filepath, blank=True)
    video=models.FileField(upload_to=upload_filepath, blank=True)

    def __str__(self):
        return f'[{self.id}] {self.title}'
    
class Like(models.Model):
    user=models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="user_likes")
    post=models.ForeignKey(to=Post, on_delete=models.CASCADE, related_name="post_likes")
    
class PostCategory(models.Model): #중간테이블
    post=models.ForeignKey(to=Post, on_delete=models.CASCADE, related_name="post_categories")
    category=models.ForeignKey(to=Category, on_delete=models.CASCADE, related_name="post_categories")
    
class Comment(models.Model):
    post=models.ForeignKey(to=Post, on_delete=models.CASCADE, related_name="comments")
    content=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    author=models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return f'[{self.id} {self.content}]'
    