from django.db import models

# Create your models here.

class Post(models.Model):
    caption = models.TextField(max_length=180)
    created_at = models.DateTimeField(auto_now_add=True)
    post_image = models.CharField(max_length=500)
    liked_by = models.ManyToManyField(
        'jwt_auth.User',
        related_name='liked_posts',
        blank=True
    )
    author = models.ForeignKey(
        'jwt_auth.User',
        related_name='posts_created',
        on_delete=models.CASCADE
    )
    
    def __str__(self) -> str:
        return f"{self.author} - {self.created_at}"
    
class Comment(models.Model):
    comment = models.TextField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(
        Post,
        related_name='comments',
        on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        'jwt_auth.User',
        related_name='comments_created',
        on_delete=models.CASCADE
    )
    
    def __str__(self) -> str:
        return f"{self.post} - {self.author}"