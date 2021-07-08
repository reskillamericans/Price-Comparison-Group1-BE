from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.TextField()
    date_created = models.DateTimeField(auto_now_add= True)
    date_updated = models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return self.name

class LikeButton(models.Model):
    content=models.TextField(null=True)
    likes = models.ManyToManyField(User, blank=True, related_name= 'likes')

    @property
    def total_likes(self):
        return self.likes.count()
