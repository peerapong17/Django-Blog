from django.shortcuts import render
from comment.models import Comment
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# Create your views here.
@login_required(login_url='loginUser')
def add_comment(request, blogId):
    if request.method == "POST":
        userId = request.user.id
        comment_message = request.POST.get("comment")
        comment = Comment.objects.create(
            user_id=userId, blog_id=blogId, comment=comment_message)
        comment.save()
    return redirect(f"/blog-detail/{blogId}")


@login_required(login_url='loginUser')
def delete_comment(request, blog_id, comment_id):
    comment = Comment.objects.get(id=comment_id)
    comment.delete()
    return redirect(f"/blog-detail/{blog_id}")