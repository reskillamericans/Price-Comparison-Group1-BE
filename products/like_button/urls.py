from django.contrib import admin
from django.urls import path
from django.conf.urls import  include #import include

urlpatterns = [
path('admin/', admin.site.urls),
path('like/',include("like.urls")),#include urls from our app
]