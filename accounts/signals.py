from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from products.models import SavedProduct

from .models import User


# Actions to perform after a User model is saved
@receiver(post_save, sender=User)
def user_saved(sender, instance, created, **kwargs):
    # Actions for newly created User
    if created:
        # Add new user to Customer group
        try:
            group = Group.objects.get(name='customer')
        except Group.DoesNotExist:
            group = Group.objects.create(name='customer')
        instance.groups.add(group)

        # Create SavedProduct list
        SavedProduct.objects.create(user=instance, name=f"{instance.username}'s list")
        print("User Created!")

    # Actions for User updates
    elif not created:
        print("User Updated")
