from django.contrib import admin
from .models import Category
class CategoryAdmin(admin.ModelAdmin):
    list_display=['name']
    list_per_page=10

admin.site.register(Category, CategoryAdmin)
