from django.contrib.auth import get_user_model
from django.db import models
from products.models import Product

User = get_user_model()

STATUS = (
    (0, "Draft"),
    (1, "Publish")

    )


# class Post(models.Model):
#    title = models.CharField(max_length=200, unique=True)
#    slug = models.SlugField(max_length=200, unique=True)
#    author = models.ForeignKey(User, on_delete= models.CASCADE,related_name='item_posts')
#    updated_on = models.DateTimeField(auto_now= True)
#    content = models.TextField()
#    created_on = models.DateTimeField(auto_now_add=True)
#    status = models.IntegerField(choices=STATUS, default=0)

#    class Meta:
#        ordering = ['-created_on']

#    def __str__(self):
#        return self.title

class Comment(models.Model):
    # name = models.CharField(max_length=80)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comment')
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)
    edited = models.BooleanField(default=False)
    edited_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.user)
