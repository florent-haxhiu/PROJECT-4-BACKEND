from django.contrib import admin
from .models import Following, Profile, Post, Comment
# Register your models here.
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Following)