from .models import Category

def categories(request):
    categories = Category.objects.all()
    return dict(categories=categories) #{"test":test}

# def all_categories(request):
#     food = Category.objects.get(id=1)
#     travel = Category.objects.get(id=2)
#     culture = Category.objects.get(id=3)
#     tradition = Category.objects.get(id=4)
#     foodLength = food.blog_set.all().count()
#     travelLength = travel.blog_set.all().count()
#     cultureLength = culture.blog_set.all().count()
#     traditionLength = tradition.blog_set.all().count()
#     # socialLength = len([a for a in blogs if a.category == "Social"])
#     # foodLength = len([a for a in blogs if a.category == "Food"])
#     # travelLength = len([a for a in blogs if a.category == "Travel"])
#     # cultureLength = len([a for a in blogs if a.category == "Culture"])
#     # traditionLength = len([a for a in blogs if a.category == "Tradition"])
#     # socialLength = len([a for a in blogs if a.category == "Social"])
#     categories = [{"name": travel, "length": travelLength},
#                   {"name": food, "length": foodLength}, {"name": culture, "length": cultureLength}, {"name": tradition, "length": traditionLength}]
#     return dict(categories=categories)