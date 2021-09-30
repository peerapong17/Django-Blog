from django.urls import path
from .views import add_comment, delete_comment

urlpatterns = [
    path("<int:blogId>", add_comment, name='addComment'),
    path("<int:blog_id>/comment/delete/<int:comment_id>",
         delete_comment, name='deleteComment'),

]
