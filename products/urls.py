from django.conf.urls import url
from django.urls import path
from .views import like_button, amazon, ebay

app_name = "products"

urlpatterns = [
    path('amazon', amazon, name='amazon'),
    path('ebay', ebay, name='ebay'),
    path('like', like_button, name='like'),
]
