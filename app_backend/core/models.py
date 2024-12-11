from django.db import models
from django.utils import timezone

class Category(models.Model):
    title = models.CharField(max_length=255, unique=True)
    image_url = models.URLField(blank=False)
    
    def __str__(self) -> str:
        return self.title
    
class Brand(models.Model):
    title = models.CharField(max_length=255, unique=True)
    image_url = models.URLField(blank=False)
    
    def __str__(self) -> str:
        return self.title
    
class Product(models.Model):
    title = models.CharField(max_length=255)
    price = models.FloatField(default=0.0, blank=False)
    description = models.TextField(max_length=550)
    is_featured = models.BooleanField(default=False)
    clothes_type = models.CharField(max_length=255, default="unisex")
    rating = models.FloatField(default=1.0, blank=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    color = models.JSONField(blank=True)
    sizes = models.JSONField(blank=True)
    image_urls = models.JSONField(blank=True)
    created_at = models.DateTimeField(blank=True)
    
    
    def __str__(self) -> str:
        return self.title