from django.db import models
from blog.models import Blog
from django.contrib.auth.models import User


# Create your models here.
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, null=True)
    comment = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.userId

    class Meta:
        db_table = "comment"
        ordering = ['-created_at']