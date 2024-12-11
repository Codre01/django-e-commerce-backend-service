from rest_framework import serializers
from . import models
from core.serializers import ProductSerializer
from checkout.serializers import AddressSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(source='product_id', read_only=True)

    class Meta:
        model = models.OrderItem
        fields = ['id', 'quantity', 'price', 'size', 'color', 'product']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    address = AddressSerializer(read_only=True)

    class Meta:
        model = models.Order
        fields = [
            'id', 
            'total_amount', 
            'status', 
            'payment_status', 
            'created_at', 
            'updated_at',
            'items',
            'address'
        ]
