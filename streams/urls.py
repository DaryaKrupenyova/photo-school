from django.urls import path

from .views import stream_page

urlpatterns = [
    path('stream_page/', stream_page),
]