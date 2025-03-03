from re import search

from django.shortcuts import render, HttpResponse, redirect
from django.template.defaultfilters import title
from unicodedata import category

from posts.forms import PostCreateForm, SearchForm, PostUpdateForm
from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.generic import ListView, DetailView, CreateView
from django.db.models import Q
from .models import Post
import random


"""

posts = [post1, post2, post3, post4, post5, post6, post7, post8, post9, post10]
limit = 2
page = 3

start = (page - 1) * limit
end = start + limit

start = (3 - 1) * 2 = 4
end = 4 + 2 = 6

"""




# Create your views here.


def test_view(request):
    return HttpResponse(f"Hello World {random.randint(0, 100)}")

def html_view(request):
    if request.method == "GET":
        return render(request, "main.html")
    else:
        return HttpResponse("Hello World")

class TestView(View):
    def get(self, request):
        return HttpResponse(f"Hello World {random.randint(0, 100)}")


@login_required(login_url="/login/")
def post_list_view(request):
    form = SearchForm()
    query_params = request.GET # - Здесь мы получаем ключ и значение, которые передали в url
    limit = 3

    if request.method == "GET":
        posts = Post.objects.all()
        search = query_params.get("search")
        category_id = query_params.get("category")
        tags = query_params.getlist("tags")
        ordering = query_params.get("ordering")
        page = int(query_params.get("page")) if query_params.get("page") else 1


        if search:
            posts = Post.objects.filter(Q(title__icontains=search) | Q(content__icontains=search))

        if category_id:
            posts = posts.filter(category_id=category_id)

        if tags:
            tags = [int(tag) for tag in tags]
            posts = posts.filter(tags__id__in=tags)

        if ordering:
            posts = posts.order_by(ordering) # order_by - сортировка по полю

        max_pages = posts.count() / limit
        # posts = 12 / 3 = 4.0

        if round(max_pages) < max_pages:
            max_pages = round(max_pages + 1)

        else:
            max_pages = round(max_pages)

        start = (page - 1) * limit
        end = start + limit

        posts = posts[start:end] # slice - start, end, step

        print(posts)

        print(max_pages)

        context = {
            "posts": posts,
            "form": form,
            "max_pages": range(1, max_pages + 1),
        }

        return render(request, "posts/post_list.html", context = context)
    else:
        return HttpResponse("Hello World")


class PostListView(ListView):
    model = Post
    template_name = "posts/post_list.html"
    context_object_name = "posts"
    paginate_by = 3

    def get_queryset(self):
        query_params = self.request.GET
        queryset = Post.objects.all()

        search = query_params.get("search")
        category_id = query_params.get("category")
        tags = query_params.getlist("tags")
        ordering = query_params.get("ordering")

        if search:
            queryset = queryset.filter(Q(title__icontains=search) | Q(content__icontains=search))

        if category_id:
            queryset = queryset.filter(category_id=category_id)

        if tags:
            tags = [int(tag) for tag in tags]
            queryset = queryset.filter(tags__id__in=tags)

        if ordering:
            queryset = queryset.order_by(ordering)

        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context["form"] = SearchForm()
        return context



@login_required(login_url="/login/")
def post_detail_view(request, post_id):
    if request.method == "GET":
        post = Post.objects.get(id=post_id)
        context = {
            "post": post
        }
        return render(request, "posts/post_detail.html", context = context)


class PostDetailView(DetailView):
    model = Post
    template_name = "posts/post_detail.html"
    context_object_name = "post"
    pk_url_kwarg = "post_id"



@login_required(login_url="/login/")
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

class PostCreateView(CreateView):
    model = Post
    success_url = "/posts/class/"
    form_class = PostUpdateForm
    template_name = "posts/post_create.html"


@login_required(login_url="/login/")
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


@login_required(login_url="/login/")
def post_update_view(request, post_id):
    try:
        post = Post.objects.get(id=post_id, author=request.user)
    except Post.DoesNotExist:
        return HttpResponse("Post not found")

    if request.method == "GET":
        form = PostUpdateForm(instance=post)
        return render(request, "posts/post_update.html", context={"form": form})

    if request.method == "POST":
        form = PostUpdateForm(request.POST, request.FILES, instance=post)
        if not form.is_valid():
            return render(request, "posts/post_update.html", context={"form": form})
        elif form.is_valid():
            form.save()
            return redirect("/profile/")
        else:
            return HttpResponse("Post not updated")

