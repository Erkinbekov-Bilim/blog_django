"""
URL configuration for blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from blog import settings
from posts.views import (test_view, html_view, post_list_view,
                         post_detail_view, post_create_view,
                         post_create_django_view, post_update_view, TestView, PostListView, PostDetailView, PostCreateView)

from users.views import register_view, login_view, logout_view, profile_view
from django.conf.urls.static import static

urlpatterns = ([
    path("posts/create/class/", PostCreateView.as_view()),
    path("posts/<int:post_id>/class/", PostDetailView.as_view()),
    path("posts/class/", PostListView.as_view()),
    path("test/class/", TestView.as_view()),
    path("admin/", admin.site.urls),
    path("test/", test_view),
    path("posts/", post_list_view),
    path("posts/<int:post_id>/", post_detail_view),
    path("posts/create/", post_create_view),
    path("posts/create/django/", post_create_django_view),
    path("register/", register_view),
    path("login/", login_view),
    path("logout/", logout_view),
    path("profile/", profile_view),
    path("posts/<int:post_id>/update/", post_update_view),
    path('', html_view),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))

