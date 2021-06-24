from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):
    """
    User model inherited from AbstractUser. Adds email field to User.
    """
    # The following are inherited from AbstractUser:
    # username (required), password (required)
    # first_name (optional), last_name (optional)

    # Make email required and unique
    email = models.EmailField(_('email address'), blank=False, unique=True,
                              help_text="Required.")

    def __str__(self):
        return self.username

#
# class Customer(models.Model):
#     """
#     Customer model to keep track of products and other data
#     """
#     user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
#     # profile_pic = models.ImageField(default="profile1.png", null=True, blank=True)
#
#     def __str__(self):
#         return self.user
