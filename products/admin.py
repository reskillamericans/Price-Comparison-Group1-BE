from django.contrib import admin
from .models import Product, LikeButton, SavedProduct
# Register your models here.

admin.site.register(Product)
admin.site.register(LikeButton)
admin.site.register(SavedProduct)
