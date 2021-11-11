from django.contrib import admin
from .models import Comment


# Register your models here.
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'blog', 'comment', 'created_at']
    list_per_page = 10


admin.site.register(Comment, CommentAdmin)
