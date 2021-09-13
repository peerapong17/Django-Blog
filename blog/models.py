from django.db import models


class Blog(models.Model):
    title = models.CharField(max_length=250)
    content = models.TextField()
    userId = models.IntegerField(default=False)
    writer = models.CharField(max_length=50, default="Anonymous")
    category = models.CharField(max_length=20, null=True)
    image = models.ImageField(upload_to='uploads/', blank=True)
    likes = models.JSONField(default=[])
    views = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Comments(models.Model):
    userId = models.IntegerField(default=False)
    username = models.TextField(default="anonymous")
    blogId = models.IntegerField(default=False)
    comment = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
