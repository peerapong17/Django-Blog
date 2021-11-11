from .models import Blog
from category.models import Category
from comment.models import Comment
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.core import serializers as core_serializers
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404



@login_required(login_url="login")
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

    return render(request, "main/index.html", {"blogs": blogsPerPage, "page": page, "popularBlogs": popularBlogs})


@login_required(login_url='login')
def blogAdmin(request):
    return render(request, "blog-admin/index.html")


@login_required(login_url='login')
def create_blog(request):

    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        imageFile = request.FILES['image']
        category = request.POST['category']
        writer_id = request.user.id
        fs = FileSystemStorage()
        img_url = "uploads/" + imageFile.name
        fs.save(img_url, imageFile)

        blog = Blog.objects.create(
            title=title, content=content, image=img_url, category_id=category, writer_id=writer_id)
        blog.save()
        return JsonResponse({"message": "Blog created successfully"})

    return render(request, "main/create.html")


@login_required(login_url='login')
def user_blog(request):
    user_id = request.user.id
    # blogsnaja = Blog.objects.filter(writer_id=user_id).all().order_by("-pk")
    # user = User.objects.filter(id=user_id).first()
    user = get_object_or_404(User, id=user_id)
    blogs = user.blog_set.all()
    return render(request, "main/user_blog.html", {"blogs": blogs})


def get_blogs(request):
    blog = Blog.objects.all()
    data = core_serializers.serialize('json', blog)
    return HttpResponse(data, content_type="application/json")


def get_blog(request, blog_id):
    blog = Blog.objects.get(id=blog_id)
    data = core_serializers.serialize('json', [blog])
    return HttpResponse(data, content_type="application/json")


@login_required(login_url='login')
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

    return render(request, "main/update.html", {"blog": blog})


@login_required(login_url='login')
def updateBlogAdmin(request, blogId):
    fs = FileSystemStorage()
    blog = get_object_or_404(Blog, id=blogId)
    if request.method == "POST":
        blog.title = request.POST.get('title')
        blog.content = request.POST.get('content')
        blog.category_id = request.POST['category']
        print(request.POST['category'])

        if request.FILES:
            imageFile = request.FILES['image']

            fs.delete(str(blog.image))

            img_url = "uploads/" + imageFile.name
            fs.save(img_url, imageFile)

            blog.image = img_url

        blog.save()

        return redirect("blog_admin")

    return render(request, "blog-admin/update.html", {"blog": blog})


@login_required(login_url='login')
def blog_detail(request, blog_id):
    blog = Blog.objects.filter(id=blog_id).first()
    # print(get_object_or_404(Blog, id=blog_id))
    blog.views += 1
    blog.save()
    comments = blog.comment_set.all().order_by("created_at")
    return render(request, "main/detail.html", {"blog": blog, "comments": comments})


@login_required(login_url='login')
def delete_blog(request, blogId):
    fs = FileSystemStorage()
    blog = Blog.objects.get(id=blogId)
    fs.delete(str(blog.image))
    blog.delete()
    return redirect("userBlog")


@login_required(login_url='login')
def like_blog(request, blog_id):
    blog = Blog.objects.get(id=blog_id)
    userId = request.user.id
    if len(blog.likes) != 0:
        if userId in blog.likes:
            index = blog.likes.index(userId)
            blog.likes.pop(index)
        else:
            blog.likes.append(userId)
        blog.save()

        json_decoded = core_serializers.serialize("json", [blog])
        return HttpResponse(json_decoded, content_type="application/json")
        # return JsonResponse(blog, safe=False)

    else:
        blog.likes.append(userId)
        blog.save()

        json_decoded = core_serializers.serialize("json", [blog])
        return HttpResponse(json_decoded, content_type="application/json")
        # return JsonResponse(blog, safe=False)


@login_required(login_url='login')
def like_blog_detail(request, blog_id):
    blog = Blog.objects.get(id=blog_id)
    userId = request.user.id
    if len(blog.likes) != 0:
        if userId in blog.likes:
            index = blog.likes.index(userId)
            blog.likes.pop(index)
        else:
            blog.likes.append(userId)
        blog.save()
        json_decoded = core_serializers.serialize("json", [blog])
        return HttpResponse(json_decoded, content_type="application/json")
    else:
        blog.likes.append(userId)
        blog.save()
        json_decoded = core_serializers.serialize("json", [blog])
        return HttpResponse(json_decoded, content_type="application/json")
    # return redirect(f"/blog-detail/{blog_id}")


def test(request):
    return render('test/testnaja.html')
