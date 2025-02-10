from django.shortcuts import render, HttpResponse
from .models import Post
import random

# Create your views here.


def test_view(request):
    return HttpResponse(f"Hello World {random.randint(0, 100)}")

def html_view(request):
    return render(request, "main.html")


def post_list_view(request):
    posts = Post.objects.all()
    context = {
        "posts": posts
    }
    return render(request, "posts/post_list.html", context = context)

def post_detail_view(request, id):
    post = Post.objects.get(id=id)
    context = {
        "post": post
    }
    return render(request, "posts/post_detail.html", context = context)