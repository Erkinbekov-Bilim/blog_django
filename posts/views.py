from django.shortcuts import render, HttpResponse, redirect
from posts.forms import PostCreateForm
from .models import Post
import random



# Create your views here.


def test_view(request):
    return HttpResponse(f"Hello World {random.randint(0, 100)}")

def html_view(request):
    if request.method == "GET":
        return render(request, "main.html")
    else:
        return HttpResponse("Hello World")


def post_list_view(request):
    if request.method == "GET":
        posts = Post.objects.all()
        context = {
            "posts": posts
        }
        return render(request, "posts/post_list.html", context = context)
    else:
        return HttpResponse("Hello World")

def post_detail_view(request, id):
    post = Post.objects.get(id=id)
    context = {
        "post": post
    }
    return render(request, "posts/post_detail.html", context = context)


def post_create_view(request):
    if request.method == "GET":
        return render(request, "posts/post_create.html")
    elif request.method == "POST":
        data = request.POST
        title = data.get("title")
        content = data.get("content")
        image = request.FILES.get("image")
        post = Post.objects.create(title=title, content=content, image=image)
        if post:
            return redirect("/posts/")
        else:
            return HttpResponse("Post not created")


def post_create_django_view(request):
    if request.method == "GET":
        form = PostCreateForm()
        return render(request, "posts/post_create_django.html",context= {"form": form})
    elif request.method == "POST":
        form = PostCreateForm(request.POST, request.FILES)

        if not form.is_valid():
            return render(request, "posts/post_create_django.html",context= {"form": form})

        elif form.is_valid():
            title = form.cleaned_data.get("title")
            content = form.cleaned_data.get("content")
            image = form.cleaned_data.get("image")
            post = Post.objects.create(title=title, content=content, image=image)

        if post:

            return redirect("/posts/")
        else:
            return HttpResponse("Post not created")