from .models import Blog
from category.models import Category
from comment.models import Comment
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.core import serializers as core_serializers
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404


@login_required(login_url='loginUser')
def home(request, category_id=None, writer=None):
    blogs = False
    popularBlogs = Blog.objects.all().order_by("-views")[:3]
    if category_id:
        blogs = Category.objects.get(id=category_id).blog_set.all()
    elif writer:
        blogs = Blog.objects.filter(
            writer__username=writer).all().order_by("-pk")
    else:
        blogs = Blog.objects.all().order_by("-pk")

    paginator = Paginator(blogs, 3)

    try:
        page = int(request.GET.get("page"))
    except:
        page = 1

    try:
        blogsPerPage = paginator.get_page(page)
    except:
        blogsPerPage = paginator.get_page(1)

    if request.method == "POST":
        searchInput = (request.POST['search'])
        # basic way
        # allBlogs = Blog.objects.all()
        # blogs = [blog for blog in allBlogs if searchInput.lower()
        #          in blog.title.lower()]

        # another way
        blogs = Blog.objects.filter(title__contains=searchInput).all()

        paginator = Paginator(blogs, 3)

        try:
            page = int(request.GET.get("page"))
        except:
            page = 1

        try:
            blogsPerPage = paginator.get_page(page)
        except:
            # blogsPerPage = paginator.get_page(1)
            blogsPerPage = paginator.get_page(paginator.num_pages)

    return render(request, "main/home.html", {"blogs": blogsPerPage, "page": page, "popularBlogs": popularBlogs})


@login_required(login_url='loginUser')
def create_blog(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        image = request.FILES['image']
        category = request.POST['category']
        writer_id = request.user.id

        blog = Blog.objects.create(
            title=title, content=content, image=image, category_id=category, writer_id=writer_id)
        blog.save()
        return JsonResponse({"message": "Blog created successfully"})

    return render(request, "main/create_blog.html")


@login_required(login_url='loginUser')
def user_blog(request):
    user_id = request.user.id
    # blogsnaja = Blog.objects.filter(writer_id=user_id).all().order_by("-pk")
    # user = User.objects.filter(id=user_id).first()
    user = get_object_or_404(User, id=user_id)
    blogs = user.blog_set.all()
    return render(request, "main/user_blog.html", {"blogs": blogs})


def get_blog_by_id(request, blogId):
    blog = Blog.objects.all()
    data = core_serializers.serialize('json', blog)
    return HttpResponse(data, content_type="application/json")


@login_required(login_url='loginUser')
def update_blog(request, blogId):
    # blog = Blog.objects.get(id=blogId)
    blog = get_object_or_404(Blog, id=blogId)
    if request.method == "POST":
        blog = Blog.objects.get(id=blogId)
        blog.title = request.POST.get('title')
        blog.content = request.POST.get('content')
        blog.category_id = request.POST['category']

        if request.FILES:
            blog.image = request.FILES['image']
        blog.save()
        return JsonResponse({"message": "Blog updated successfully"})

    return render(request, "main/update_blog.html", {"blog": blog})


@login_required(login_url='loginUser')
def blog_detail(request, blog_id):
    blog = Blog.objects.filter(id=blog_id).first()
    # print(get_object_or_404(Blog, id=blog_id))
    blog.views += 1
    blog.save()
    comments = blog.comment_set.all()
    return render(request, "main/blog_detail.html", {"blog": blog, "comments": comments})


@login_required(login_url='loginUser')
def delete_blog(request, blogId):
    blog = Blog.objects.get(id=blogId)
    blog.delete()
    return redirect("userBlog")


@login_required(login_url='loginUser')
def like_blog(request, blogId):
    blog = Blog.objects.get(id=blogId)
    userId = request.user.id
    if len(blog.likes) != 0:
        if userId in blog.likes:
            index = blog.likes.index(userId)
            blog.likes.pop(index)
        else:
            blog.likes.append(userId)
        blog.save()
    else:
        blog.likes.append(userId)
        blog.save()
    return redirect("home")


@login_required(login_url='loginUser')
def like_blog_detail(request, blogId):
    blog = Blog.objects.get(id=blogId)
    userId = request.user.id
    if len(blog.likes) != 0:
        if userId in blog.likes:
            index = blog.likes.index(userId)
            blog.likes.pop(index)
        else:
            blog.likes.append(userId)
        blog.save()
    else:
        blog.likes.append(userId)
        blog.save()
    return redirect(f"/blog-detail/{blogId}")

def test(request):
    return render('test/testnaja.html')
