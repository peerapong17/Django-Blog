
from django.urls import path
from .views import home, create_blog, blog_detail, user_blog, update_blog, delete_blog, add_comment, like_blog, like_blog_detail, blog_filtered_by_category, blog_filtered_by_writer, get_blog_by_id, delete_comment

urlpatterns = [
    path("", home, name="home"),
    path("create-blog", create_blog),
    path("blog-detail/<int:blogId>", blog_detail, name="blogDetail"),
    path("user-blog", user_blog, name='userBlog'),
    path("update-blog/<int:blogId>", update_blog, name='updateBlog'),
    path("get-blog/<int:blogId>", get_blog_by_id),
    path("delete-blog/<int:blogId>", delete_blog, name='deleteBlog'),
    path("comment/<int:blogId>", add_comment, name='addComment'),
    path("<int:blog_id>/comment/delete/<int:comment_id>", delete_comment, name='deleteComment'),
    path("like/<int:blogId>", like_blog, name='likeBlog'),
    path("like/blog/<int:blogId>", like_blog_detail, name='likeBlogInBlogDetail'),
    path("blog/writer/<str:writer>", blog_filtered_by_writer,
         name="blogFilteredByWriter"),
    path("blog/category/<int:category_id>", blog_filtered_by_category,
         name="blogFilteredByCategory"),
]
