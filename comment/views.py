import json

from django.http import HttpResponse, JsonResponse
from comment.models import Comment
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.core import serializers as core_serializers


# Create your views here.
@login_required(login_url='login')
def add_comment(request, blog_id):
    if request.method == "POST":
        userId = request.user.id
        comment_input = request.POST['comment']
        comment = Comment.objects.create(
            user_id=userId, blog_id=blog_id, comment=comment_input)
        comment.save()

        data_response = {
            "id": comment.id,
            "user": comment.user.username,
            "comment": comment.comment,
            "created_at": str(comment.created_at)
        }

        # if data did not come from the database we don't have to do this
        # data = core_serializers.serialize('json', [data_response])

        return HttpResponse(json.dumps(data_response), content_type="application/json")


@login_required(login_url='login')
def delete_comment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    comment.delete()
    return JsonResponse("success", safe=False)
