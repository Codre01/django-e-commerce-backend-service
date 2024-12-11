from django.db import models
from django.contrib.auth.models import User
from core.models import Product

class WishList(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return "{}/{}".format(self.user_id.username, self.product.title)
