
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("blog-admin", views.blogAdmin, name="blog_admin"),
    path("create-blog", views.create_blog, name="createBlog"),
    path("blog-detail/<int:blog_id>", views.blog_detail, name="blogDetail"),
    path("user-blog", views.user_blog, name='userBlog'),
    path("update-blog/<int:blogId>", views.update_blog, name='updateBlog'),
    path("update-blog-admin/<int:blogId>", views.updateBlogAdmin, name='update_blog_admin'),
    path("get-blogs/", views.get_blogs),
    path("get-blog/<int:blog_id>", views.get_blog),
    path("delete-blog/<int:blogId>", views.delete_blog, name='deleteBlog'),
    path("like/<int:blog_id>", views.like_blog, name='likeBlog'),
    path("like/blog/<int:blog_id>", views.like_blog_detail, name='likeBlogDetail'),
    path("category/<int:category_id>", views.home,
         name="get_blogs_by_category"),
    path("writer/<str:writer>", views.home,
         name="get_blogs_by_writer"),
    path("test", views.test,
         name="get_blogs_by_writer"),

]
