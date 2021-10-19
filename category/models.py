from django.db import models
from django.urls import reverse

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "category"
        ordering = ['id']

    def blog_length_in_this_category(self):
        length = self.blog_set.all().count()
        return length

    def get_blogs_by_category(self):
        return reverse('get_blogs_by_category',args=[self.id])

    def update_category(self):
        return reverse('update_category',args=[self.id])

    def delete_category(self):
        return reverse('delete_category',args=[self.id])
