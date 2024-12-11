from rest_framework import serializers
from core.models import Product, Category, Brand

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'image_url']

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'title', 'image_url']

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    brand = BrandSerializer(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'description', 'is_featured', 'clothes_type', 'rating', 'category', 'brand', 'color', 'sizes', 'image_urls', 'created_at']