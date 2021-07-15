from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Product, LikeButton


# Actions to perform after a Product is saved
@receiver(post_save, sender=Product)
def product_saved(sender, instance, created, **kwargs):
    # Actions for newly created User
    if created:
        # Create LikeButton list
        LikeButton.objects.create(product=instance)
        print("Product Created!")

    # Actions for User updates
    elif not created:
        print("Product Updated")
