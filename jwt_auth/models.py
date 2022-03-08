from distutils.command.upload import upload
from email.policy import default
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    profile_image = models.ImageField(upload_to='media/', default='profilePic.png')
    bio = models.TextField(max_length=180)
    is_private = models.BooleanField(default=False)
    followed_by = models.ManyToManyField(
        'jwt_auth.User',
        related_name='follows',
        blank=True,
    )
    
class DM(models.Model):
    message = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    send = models.ForeignKey(
        User,
        related_name='message_created',
        on_delete=models.CASCADE,
    )
    recipient = models.ForeignKey(
        User,
        related_name='message_got',
        on_delete=models.CASCADE,
    )
    
    def __str__(self) -> str:
        return f"{self.sender} -- {self.recipient} -> {self.created_at}"