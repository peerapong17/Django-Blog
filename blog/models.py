from django.db import models
from django.urls import reverse
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
        db_table = "blog"
        ordering = ['-created_at']

    def get_blogs_by_writer(self):
        return reverse('get_blogs_by_writer', args=[self.writer.username])

    def update_blog_admin(self):
        return reverse('update_blog_admin', args=[self.id])

    def delete_blog(self):
        return reverse('deleteBlog', args=[self.id])
