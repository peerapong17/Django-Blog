
from django.urls import path
from .views import home, create_blog, blog_detail, user_blog, update_blog, delete_blog,  like_blog, like_blog_detail, get_blog_by_id

urlpatterns = [
    path("", home, name="home"),
    path("create-blog", create_blog),
    path("blog-detail/<int:blog_id>", blog_detail, name="blogDetail"),
    path("user-blog", user_blog, name='userBlog'),
    path("update-blog/<int:blogId>", update_blog, name='updateBlog'),
    path("get-blog/<int:blogId>", get_blog_by_id),
    path("delete-blog/<int:blogId>", delete_blog, name='deleteBlog'),
    path("like/<int:blogId>", like_blog, name='likeBlog'),
    path("like/blog/<int:blogId>", like_blog_detail, name='likeBlog'),
    path("category/<int:category_id>", home,
         name="get_blogs_by_category"),
    path("writer/<str:writer>", home,
         name="get_blogs_by_writer"),

]
