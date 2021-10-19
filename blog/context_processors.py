

from blog.models import Blog


def blogsAdmin(request):
    blogsAdmin = Blog.objects.all()
    return dict(blogsAdmin=blogsAdmin)
