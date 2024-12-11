from rest_framework import serializers
from . import models

class WishListSerializers(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='product.id')
    title = serializers.ReadOnlyField(source='product.title')
    description = serializers.ReadOnlyField(source='product.description')
    price = serializers.ReadOnlyField(source='product.price')
    is_featured = serializers.ReadOnlyField(source='product.is_featured')
    clothes_type = serializers.ReadOnlyField(source='product.clothes_type')
    rating = serializers.ReadOnlyField(source='product.rating')
    category = serializers.ReadOnlyField(source='product.category.id')
    brand = serializers.ReadOnlyField(source='product.brand.id')
    color = serializers.ReadOnlyField(source='product.color')
    sizes = serializers.ReadOnlyField(source='product.sizes')
    image_urls = serializers.ReadOnlyField(source='product.image_urls')
    created_at = serializers.ReadOnlyField(source='product.created_at')

    class Meta:
        model = models.WishList
        fields = ['id', 'title', 'description', 'price', 'is_featured', 'clothes_type', 'rating', 'category', 'brand', 'color', 'sizes', 'image_urls', 'created_at']