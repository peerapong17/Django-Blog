from django.urls import path
from .views import add_comment, delete_comment

urlpatterns = [
    path("<int:blog_id>", add_comment, name='addComment'),
    path("delete/<int:comment_id>",
         delete_comment, name='deleteComment'),

]
