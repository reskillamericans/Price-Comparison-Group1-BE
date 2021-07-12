from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils.translation import ugettext_lazy as _


class CaseInsensitiveUserManager(UserManager):
    def get_by_natural_key(self, username):
        """
        By default, Django does a case-sensitive check on usernames.
        Overriding this method fixes it.
        """
        return self.get(**{self.model.USERNAME_FIELD + '__iexact': username})


class User(AbstractUser):
    """
    User model inherited from AbstractUser. Adds email field to User.
    The following are inherited from AbstractUser:
    username (required), password (required), first_name (optional), last_name (optional)
    """

    # Use new manager
    objects = CaseInsensitiveUserManager()

    # Make email required and unique
    email = models.EmailField(_('email address'), blank=False, unique=True,
                              help_text="Required.")

    # Possible profile picture if there's time
    #     # profile_pic = models.ImageField(default="profile1.png", null=True, blank=True)

    def __str__(self):
        return self.username
