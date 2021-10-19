from django.shortcuts import get_object_or_404, redirect, render

from category.models import Category

# Create your views here.


def index(request):
    return render(request, "category/index.html")


def createCategory(request):
    if request.method == "POST":
        name = request.POST['name']
        category = Category(name=name)
        category.save()
        return redirect("categories")

    return render(request, "category/create.html")


def updateCategory(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == "POST":
        category.name = request.POST['name']
        category.save()
        return redirect("categories")

    return render(request, "category/update.html", {"category": category})


def deleteCategory(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.delete()
    return redirect("categories")
