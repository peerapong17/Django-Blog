from blog.models import Blog
from django.contrib import admin
from .models import Blog



class BlogAdmin(admin.ModelAdmin):
    list_display=['title','writer','category','image', "likes", "created_at"]
    list_editable=['writer','category']
    list_per_page=10


admin.site.register(Blog, BlogAdmin)
