from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from users.forms import RegisterForm, LoginForm
from django.contrib.auth import login, authenticate, logout
from  users.models import Profile

# Create your views here.


def register_view(request):
    if request.method == "GET":
        form = RegisterForm()
        return render(request, "users/register.html", context={"form": form})
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)
        if not form.is_valid():
            return render(request, "users/register.html", context={"form": form})
        elif form.is_valid():
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            avatar = form.cleaned_data.get("avatar")
            age = form.cleaned_data.get("age")

            if not User.objects.filter(email=email).exists():
                user = User.objects.create_user(username=username, email=email, password=password)

                if user:
                    Profile.objects.create(user=user, age=age, avatar=avatar)
                elif not user:
                    form.add_error(None, "Unknown error")
                    return render(request, "users/register.html", context={"form": form})

                return redirect("/login/")

            else:
                 form.add_error(None, "User with this email already exists")
                 return render(request, "users/register.html", context={"form": form})




def login_view(request):
    if request.method == "GET":
        form = LoginForm()
        return render(request, "users/login.html", context={"form": form})
    if request.method == "POST":
        form = LoginForm(request.POST)
        if not form.is_valid():
            return render(request, "users/login.html", context={"form": form})
        elif form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            user = authenticate(username=username, password=password)

            if user:
                login(request, user)
                return redirect("/")
            if not user:
                form.add_error(None, "Invalid username or password")
                return render(request, "users/login.html", context={"form": form})


def logout_view(request):
    logout(request)
    return redirect("/")


def profile_view(request):
    if request.method == "GET":
        user = request.user
        posts = user.posts.all()
        return render(request, "users/profile.html", context={"user": user, "posts": posts})




