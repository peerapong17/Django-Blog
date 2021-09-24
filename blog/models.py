from django.db import models
from category.models import Category
from django.contrib.auth.models import User


class Blog(models.Model):
    title = models.CharField(max_length=250)
    content = models.TextField()
    writer = models.ForeignKey(
        User, on_delete=models.PROTECT, default="Anonymous")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True)
    image = models.ImageField(upload_to='uploads/', blank=True)
    likes = models.JSONField(default=[])
    views = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    username = models.TextField(default="anonymous")
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, null=True)
    comment = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.userId

    class Meta:
        ordering = ['-created_at']
