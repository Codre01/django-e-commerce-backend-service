from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from core.models import Product

# Create your models here.
class Cart(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    size = models.CharField(max_length=255, blank=False)
    color = models.CharField(max_length=255, blank=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return '{}/{}'.format(self.user_id.username, self.product.title)
