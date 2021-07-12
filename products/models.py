from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    amazon_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    ebay_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.name


class SavedProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, related_name='savedproducts', blank=True)
    name = models.CharField(max_length=50, blank=True, default=f'My List')

    def __str__(self):
        return self.name


class LikeButton(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    user = models.ManyToManyField(User, blank=True, related_name='likebutton')

    # content = models.TextField(null=True)

    def __str__(self):
        return f"{self.product.name} Likes"

    @property
    def total_likes(self):
        return self.user.count()
