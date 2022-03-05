from distutils.command.upload import upload
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(blank=True, upload_to="media/", default="media/profilePic.png")
    bio = models.CharField(max_length=255)
    
    def __str__(self) -> str:
        return f"{self.user.username}"
    
class Post(models.Model):
    post_image = models.ImageField(upload_to="media/post")
    caption = models.CharField(blank=True, max_length=180)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    like = models.IntegerField(default=0)
    
    def __str__(self) -> str:
        return f"{self.profile.user.username}"

class Following(models.Model):
    username = models.CharField(blank=True, max_length=180)
    followed = models.CharField(blank=True, max_length=180)
    
    def __str__(self) -> str:
        return f"{self.username}"
    
class Comment(models.Model):
    post = models.IntegerField(default=0)
    username = models.CharField(blank=True, max_length=180)
    comment = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    count = models.IntegerField(default=0)
    
    def __str__(self) -> str:
        return f"{self.username}"