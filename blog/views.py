from category.models import Category
from django.core import serializers as core_serializers
from .models import Comment, Blog
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required


@login_required(login_url='loginUser')
def home(request):
    blogs = Blog.objects.all().order_by("-pk")
    popularBlogs = Blog.objects.all().order_by("-views")[:3]
    food = Category.objects.get(id=1)
    travel = Category.objects.get(id=2)
    culture = Category.objects.get(id=3)
    tradition = Category.objects.get(id=4)
    foodLength = food.blog_set.all().count()
    travelLength = travel.blog_set.all().count()
    cultureLength = culture.blog_set.all().count()
    traditionLength = tradition.blog_set.all().count()
    # socialLength = len([a for a in blogs if a.category == "Social"])
    # foodLength = len([a for a in blogs if a.category == "Food"])
    # travelLength = len([a for a in blogs if a.category == "Travel"])
    # cultureLength = len([a for a in blogs if a.category == "Culture"])
    # traditionLength = len([a for a in blogs if a.category == "Tradition"])
    # socialLength = len([a for a in blogs if a.category == "Social"])
    categories = [{"name": travel, "length": travelLength},
                  {"name": food, "length": foodLength}, {"name": culture, "length": cultureLength}, {"name": tradition, "length": traditionLength}]
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
        allBlogs = Blog.objects.all()
        blogs = [blog for blog in allBlogs if searchInput.lower()
                 in blog.title.lower()]
        paginator = Paginator(blogs, 3)

        try:
            page = int(request.GET.get("page"))
        except:
            page = 1

        try:
            blogsPerPage = paginator.get_page(page)
        except:
            blogsPerPage = paginator.get_page(1)

    return render(request, "main/home.html", {"blogs": blogsPerPage, "categories": categories, "page": page, "popularBlogs": popularBlogs})


@login_required(login_url='loginUser')
def create_blog(request):
    categories = Category.objects.all()
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        image = request.FILES['image']
        category = request.POST['category']
        userId = request.user.id
        writer = request.user.username

        blog = Blog.objects.create(
            title=title, content=content, userId=userId, image=image, category_id=category, writer=writer)
        blog.save()
        return JsonResponse({"message": "Blog created successfully"})

    return render(request, "main/create_blog.html", {"categories": categories})


@login_required(login_url='loginUser')
def user_blog(request):
    userId = request.user.id
    blogs = Blog.objects.filter(userId=userId).all().order_by("-pk")
    return render(request, "main/user_blog.html", {"blogs": blogs})


def get_blog_by_id(request, blogId):
    blog = Blog.objects.all()
    data = core_serializers.serialize('json', blog)
    return HttpResponse(data, content_type="application/json")


@login_required(login_url='loginUser')
def update_blog(request, blogId):
    blog = Blog.objects.get(id=blogId)
    categories = Category.objects.all()
    if request.method == "POST":
        blog = Blog.objects.get(id=blogId)
        blog.title = request.POST.get('title')
        blog.content = request.POST.get('content')
        blog.category = request.POST['category']

        if request.FILES:
            blog.image = request.FILES['image']
        blog.save()
        return JsonResponse({"message": "Blog updated successfully"})

    return render(request, "main/update_blog.html", {"categories": categories, "blog": blog})


@login_required(login_url='loginUser')
def blog_detail(request, blogId):
    blog = Blog.objects.filter(id=blogId).first()
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
def add_comment(request, blogId):
    userId = request.user.id
    username = request.user.username
    comment = Comment.objects.create(
        userId=userId, username=username, blog_id=blogId, comment=request.GET.get("comment"))
    comment.save()
    return redirect(f"/blog-detail/{blogId}")


@login_required(login_url='loginUser')
def delete_comment(request, blog_id, comment_id):
    comment = Comment.objects.get(id=comment_id)
    comment.delete()
    return redirect(f"/blog-detail/{blog_id}")


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


@login_required(login_url='loginUser')
def blog_filtered_by_category(request, category_id):
    blogs = Category.objects.get(id=category_id).blog_set.all()
    food = Category.objects.get(id=1)
    travel = Category.objects.get(id=2)
    culture = Category.objects.get(id=3)
    tradition = Category.objects.get(id=4)
    foodLength = Category.objects.get(id=1).blog_set.all().count()
    travelLength = Category.objects.get(id=2).blog_set.all().count()
    cultureLength = Category.objects.get(id=3).blog_set.all().count()
    traditionLength = Category.objects.get(id=4).blog_set.all().count()
    popularBlogs = Blog.objects.all().order_by("-views")[:3]
    categories = [{"name": travel, "length": travelLength},
                  {"name": food, "length": foodLength}, {"name": culture, "length": cultureLength}, {"name": tradition, "length": traditionLength}]
    paginator = Paginator(blogs, 3)

    try:
        page = int(request.GET.get("page"))
    except:
        page = 1

    try:
        blogsPerPage = paginator.get_page(page)
    except:
        blogsPerPage = paginator.get_page(1)

    return render(request, "main/home.html", {"blogs": blogsPerPage, "categories": categories, "page": page, "popularBlogs": popularBlogs})


@login_required(login_url='loginUser')
def blog_filtered_by_writer(request, writer):
    blogs = Blog.objects.filter(
        writer=writer).all().order_by("-pk")
    paginator = Paginator(blogs, 3)
    popularBlogs = Blog.objects.all().order_by("-views")[:3]
    food = Category.objects.get(id=1)
    travel = Category.objects.get(id=2)
    culture = Category.objects.get(id=3)
    tradition = Category.objects.get(id=4)
    foodLength = Category.objects.get(id=1).blog_set.all().count()
    travelLength = Category.objects.get(id=2).blog_set.all().count()
    cultureLength = Category.objects.get(id=3).blog_set.all().count()
    traditionLength = Category.objects.get(id=4).blog_set.all().count()
    popularBlogs = Blog.objects.all().order_by("-views")[:3]
    categories = [{"name": travel, "length": travelLength},
                  {"name": food, "length": foodLength}, {"name": culture, "length": cultureLength}, {"name": tradition, "length": traditionLength}]

    try:
        page = int(request.GET.get("page"))
    except:
        page = 1

    try:
        blogsPerPage = paginator.get_page(page)
    except:
        blogsPerPage = paginator.get_page(1)

    return render(request, "main/home.html", {"blogs": blogsPerPage, "categories": categories, "page": page, "popularBlogs": popularBlogs})
