from django.db import models
from products.models import Product
from django.contrib.auth import get_user_model

User = get_user_model()

class Comment(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='comments', default=None, null=True, blank= True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True, default=None, related_name='user_comment')
    body = models.TextField(blank=True, null=True, default=None)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return 'Comment by {}'.format(self.user)