from rest_framework import serializers
from core.serializers import ProductSerializer
from . import models

class CartSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    
    class Meta:
        model = models.Cart
        exclude = ['user_id', 'created_at', 'updated_at']