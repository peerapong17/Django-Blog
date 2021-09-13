from threading import Timer
from django.contrib import messages
from django.core import paginator
from django.core import serializers as core_serializers
from .models import Comments, Blog
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, InvalidPage, EmptyPage


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        # user = authenticate(username="test", password="123123")
        user = User.objects.filter(username=username).first()
        if user is not None:
            login(request, user)
            return redirect('/home')
        else:
            messages.error(request, "User with given email does not exist")

    return render(request, "auth/login.html")


def register_user(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirmPassword = request.POST['confirmPassword']
        if User.objects.filter(email=email).exists():
            messages.error(request, "This email already in-use")
        elif password != confirmPassword:
            messages.error(request, "Password does not match")
        else:
            user = User.objects.create(
                username=username,
                email=email,
                password=password
            )
            user.save()
            messages.success(request, "Create account success")
            return redirect("/")
    return render(request, "auth/register.html")


def home(request):
    blogs = Blog.objects.all().order_by("-pk")
    popularBlogs = Blog.objects.all().order_by("-views")[:3]
    foodLength = len([a for a in blogs if a.category == "Food"])
    travelLength = len([a for a in blogs if a.category == "Travel"])
    cultureLength = len([a for a in blogs if a.category == "Culture"])
    traditionLength = len([a for a in blogs if a.category == "Tradition"])
    socialLength = len([a for a in blogs if a.category == "Social"])
    categories = [{"name": "Travel", "length": travelLength},
                  {"name": "Food", "length": foodLength}, {"name": "Culture", "length": cultureLength}, {"name": "Tradition", "length": traditionLength}, {"name": "Social", "length": socialLength}]
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
        blogs = Blog.objects.filter(title=searchInput).order_by("-pk")
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


def create_blog(request):
    categories = [{"name": "Travel"},
                  {"name": "Food"}, {"name": "Culture"}, {"name": "Tradition"}, {"name": "Social"}]
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        image = request.FILES['image']
        category = request.POST['category']
        userId = request.user.id
        writer = request.user.username

        blog = Blog.objects.create(
            title=title, content=content, userId=userId, image=image, category=category, writer=writer)
        blog.save()
        return JsonResponse({"message": "Blog created successfully"})

    return render(request, "main/create_blog.html", {"categories": categories})


def user_blog(request):
    userId = request.user.id
    blogs = Blog.objects.filter(userId=userId).all().order_by("-pk")
    return render(request, "main/user_blog.html", {"blogs": blogs})


def get_blog_by_id(request, blogId):
    blog = Blog.objects.all()
    data = core_serializers.serialize('json', blog)
    return HttpResponse(data, content_type="application/json")


def update_blog(request, blogId):
    categories = [{"name": "Travel"},
                  {"name": "Food"}, {"name": "Culture"}, {"name": "Tradition"}, {"name": "Social"}]
    if request.method == "POST":
        blog = Blog.objects.get(id=blogId)
        blog.title = request.POST.get('title')
        blog.content = request.POST.get('content')
        blog.category = request.POST['category']

        if request.FILES:
            blog.image = request.FILES['image']
        blog.save()
        return JsonResponse({"message": "Blog updated successfully"})

    return render(request, "main/update_blog.html", {"categories": categories})


def blog_detail(request, blogId):
    blog = Blog.objects.filter(id=blogId).first()
    blog.views += 1
    blog.save()
    comments = Comments.objects.filter(blogId=blogId).all()
    return render(request, "main/blog_detail.html", {"blog": blog, "comments": comments})


def delete_blog(request, blogId):
    blog = Blog.objects.get(id=blogId)
    blog.delete()
    return redirect("/user-blog")


def add_comment(request, blogId):
    userId = request.user.id
    username = request.user.username
    comment = Comments.objects.create(
        userId=userId, username=username, blogId=blogId, comment=request.GET.get("comment"))
    comment.save()
    return redirect(f"/blog-detail/{blogId}")


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
    return redirect("/home")


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


def blog_filtered_by_category(request, category):
    print(category)
    blogs = Blog.objects.filter(
        category=category).all().order_by("-pk")
    paginator = Paginator(blogs, 3)
    allBlogs = Blog.objects.all().order_by("-pk")
    popularBlogs = Blog.objects.all().order_by("-views")[:3]
    foodLength = len([a for a in allBlogs if a.category == "Food"])
    travelLength = len([a for a in allBlogs if a.category == "Travel"])
    cultureLength = len([a for a in allBlogs if a.category == "Culture"])
    traditionLength = len([a for a in allBlogs if a.category == "Tradition"])
    socialLength = len([a for a in allBlogs if a.category == "Social"])
    categories = [{"name": "Travel", "length": travelLength},
                  {"name": "Food", "length": foodLength}, {"name": "Culture", "length": cultureLength}, {"name": "Tradition", "length": traditionLength}, {"name": "Social", "length": socialLength}]

    try:
        page = int(request.GET.get("page"))
    except:
        page = 1

    try:
        blogsPerPage = paginator.get_page(page)
    except:
        blogsPerPage = paginator.get_page(1)

    return render(request, "main/home.html", {"blogs": blogsPerPage, "categories": categories, "page": page, "popularBlogs": popularBlogs})


def blog_filtered_by_writer(request, writer):
    print(writer)
    blogs = Blog.objects.filter(
        writer=writer).all().order_by("-pk")
    paginator = Paginator(blogs, 3)
    allBlogs = Blog.objects.all().order_by("-pk")
    popularBlogs = Blog.objects.all().order_by("-views")[:3]
    foodLength = len([a for a in allBlogs if a.category == "Food"])
    travelLength = len([a for a in allBlogs if a.category == "Travel"])
    cultureLength = len([a for a in allBlogs if a.category == "Culture"])
    traditionLength = len([a for a in allBlogs if a.category == "Tradition"])
    socialLength = len([a for a in allBlogs if a.category == "Social"])
    categories = [{"name": "Travel", "length": travelLength},
                  {"name": "Food", "length": foodLength}, {"name": "Culture", "length": cultureLength}, {"name": "Tradition", "length": traditionLength}, {"name": "Social", "length": socialLength}]

    try:
        page = int(request.GET.get("page"))
    except:
        page = 1

    try:
        blogsPerPage = paginator.get_page(page)
    except:
        blogsPerPage = paginator.get_page(1)

    return render(request, "main/home.html", {"blogs": blogsPerPage, "categories": categories, "page": page, "popularBlogs": popularBlogs})


def logout_user(request):
    logout(request)
    return redirect('/')
