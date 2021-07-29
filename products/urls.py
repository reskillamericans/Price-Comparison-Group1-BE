from django.urls import path

from .views import ProductDetailView, ProductIndexView, liked_products_view, like_button, saved_products_view, \
    add_product_view, delete_product, edit_product_view, update_product, modal_view, update_all_products

app_name = 'products'
urlpatterns = [
    # Product list
    path('', ProductIndexView.as_view(), name='index'),

    path('modal/', modal_view, name="modal"),

    # Product details
    path('<int:pk>/', ProductDetailView.as_view(), name='product'),

    # Likes
    path('like/', like_button, name='like'),
    path('liked_products/', liked_products_view, name='liked_products'),

    # Saved Products
    path('saved_products/', saved_products_view, name='saved_products'),

    # Add and Delete Product
    path('add_products/', add_product_view, name='add_products'),
    path('edit_product/', edit_product_view, name='edit_product'),
    path('update_all_products/', update_all_products, name='update_all_products'),
    path('update_product/<int:product_id>', update_product, name='update_product'),
    path('delete_product/<int:product_id>', delete_product, name='delete_product'),
    ]
