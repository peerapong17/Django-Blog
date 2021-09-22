from django.db import models
from category.models import Category


class Blog(models.Model):
    title = models.CharField(max_length=250)
    content = models.TextField()
    userId = models.IntegerField(default=False)
    writer = models.CharField(max_length=50, default="Anonymous")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True)
    image = models.ImageField(upload_to='uploads/', blank=True)
    likes = models.JSONField(default=[])
    views = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    userId = models.IntegerField(default=False)
    username = models.TextField(default="anonymous")
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, null=True)
    comment = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
