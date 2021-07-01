from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.TextField()
    date_created = models.DateTimeField(auto_now_add= True)
    date_updated = models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return self.name