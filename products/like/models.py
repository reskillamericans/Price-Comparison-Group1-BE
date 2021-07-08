from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class LikeButton(models.Model):
    content=models.TextField(null=True)
    likes = models.ManyToManyField(User, blank=True, related_name= 'likes')

    @property
    def total_likes(self):
        return self.likes.count()
