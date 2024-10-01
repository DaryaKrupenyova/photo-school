from django.urls import path, re_path

from .views import webhook_func
from django.contrib.auth import views as auth_views
from django.contrib.auth import views as dj_contrib_views

urlpatterns = [
    path('AAGvfvNqGbQyPqk0RK19CelBUzsFYVc5ffo', webhook_func),
]
