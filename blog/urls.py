
from django.urls import path
# from . views import getTheData, hello
from .views import home, login_user, register_user, logout_user, create_blog, blog_detail, user_blog, update_blog, delete_blog, add_comment, like_blog, like_blog_detail, blog_filtered_by_category, blog_filtered_by_writer, get_blog_by_id

urlpatterns = [
    path("", login_user),
    path("register", register_user),
    path("home", home, name="home"),
    path("logout", logout_user),
    path("create-blog", create_blog),
    path("blog-detail/<int:blogId>", blog_detail, name="blogDetail"),
    path("user-blog", user_blog),
    path("update-blog/<int:blogId>", update_blog),
    path("get-blog/<int:blogId>", get_blog_by_id),
    path("delete-blog/<int:blogId>", delete_blog),
    path("comment/<int:blogId>", add_comment),
    path("like/<int:blogId>", like_blog),
    path("like/blog/<int:blogId>", like_blog_detail),
    path("blog/writer/<str:writer>", blog_filtered_by_writer,
         name="blogFilteredByWriter"),
    path("blog/category/<str:category>", blog_filtered_by_category,
         name="blogFilteredByCategory"),
]
