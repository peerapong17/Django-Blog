
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="categories"),
    path("create", views.createCategory, name="create_category"),
    path("update/<int:category_id>", views.updateCategory, name="update_category"),
    path("delete/<int:category_id>", views.deleteCategory, name="delete_category"),
]
