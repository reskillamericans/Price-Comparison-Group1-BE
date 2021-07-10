from django.urls import path

from .views import *

app_name = 'products'
urlpatterns = [
    # Product details
    path('<int:pk>/', ProductDetailView.as_view(), name='product'),

    # Likes
    path('like/', like_button, name='like'),
    path('liked_products/', liked_products_view, name='liked_products'),

    # Saved Products
    path('saved_products/', saved_products_view, name='saved_products'),

    path('amazon/', amazon_view, name='amazon'),
    path('ebay/', ebay_view, name='ebay'),
    ]
