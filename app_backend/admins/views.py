from rest_framework import generics, status
from core import models, serializers as core_serializers
from . import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models import Count
from django.utils import timezone
from datetime import datetime, timedelta
from order import models as order_models, serializers as order_serializers
import random

class ProductList(APIView):
    serializer_class = serializers.ProductSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        page = int(request.query_params.get('page', 1))
        limit = 20
        offset = (page - 1) * limit

        queryset = models.Product.objects.all().annotate(product_count=Count('id'))
        queryset = list(queryset)

        random.shuffle(queryset)

        serialized_data = self.serializer_class(queryset[offset:offset+limit], many=True).data

        return Response({
            "status": "success",
            "data": serialized_data
        })


class CreateProduct(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            # Validate and fetch related category and brand
            category_id = request.data.get("category")
            brand_id = request.data.get("brand")
            
            if not category_id or not brand_id:
                return Response({
                    "status": "error",
                    "message": "Category and Brand are required fields"
                }, status=status.HTTP_400_BAD_REQUEST)

            try:
                category = models.Category.objects.get(id=category_id)
            except models.Category.DoesNotExist:
                return Response({
                    "status": "error",
                    "message": "Category not found"
                }, status=status.HTTP_404_NOT_FOUND)

            try:
                brand = models.Brand.objects.get(id=brand_id)
            except models.Brand.DoesNotExist:
                return Response({
                    "status": "error",
                    "message": "Brand not found"
                }, status=status.HTTP_404_NOT_FOUND)

            # Update request data to use IDs for foreign key relationships
            request_data = request.data.copy()
            request_data["category"] = category.id
            request_data["brand"] = brand.id

            # Ensure optional fields are in the correct format
            for field in ["color", "sizes", "image_urls"]:
                if not isinstance(request_data.get(field, []), list):
                    return Response({
                        "status": "error",
                        "message": f"{field} must be a list"
                    }, status=status.HTTP_400_BAD_REQUEST)

            # Add the creation timestamp
            request_data["created_at"] = timezone.now()

            # Serialize and validate the data
            serializer = core_serializers.ProductSerializer(data=request_data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "status": "success",
                    "message": "Product created successfully",
                    "data": serializer.data
                }, status=status.HTTP_201_CREATED)

            # Handle validation errors
            return Response({
                "status": "error",
                "message": "Invalid data provided",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            # Catch all other unexpected exceptions
            return Response({
                "status": "error",
                "message": f"An error occurred: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
class UpdateProduct(APIView):
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def put(self, request, *args, **kwargs):
        try:
            # Retrieve the product instance
            product_id = kwargs.get(self.lookup_field)
            instance = models.Product.objects.get(id=product_id)

            # Ensure `category` and `brand` are valid
            category_id = request.data.get("category", instance.category.id)
            brand_id = request.data.get("brand", instance.brand.id)

            try:
                category = models.Category.objects.get(id=category_id)
            except models.Category.DoesNotExist:
                return Response({
                    "status": "error",
                    "message": "Category not found"
                }, status=status.HTTP_404_NOT_FOUND)

            try:
                brand = models.Brand.objects.get(id=brand_id)
            except models.Brand.DoesNotExist:
                return Response({
                    "status": "error",
                    "message": "Brand not found"
                }, status=status.HTTP_404_NOT_FOUND)

            # Validate optional JSON fields
            for field in ["color", "sizes", "image_urls"]:
                if field in request.data and not isinstance(request.data[field], list):
                    return Response({
                        "status": "error",
                        "message": f"{field} must be a list"
                    }, status=status.HTTP_400_BAD_REQUEST)

            # Update request data
            request_data = request.data.copy()
            request_data["category"] = category.id
            request_data["brand"] = brand.id

            # Partial update using serializer
            serializer = core_serializers.ProductSerializer(instance, data=request_data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "status": "success",
                    "message": "Product updated successfully",
                    "data": serializer.data
                }, status=status.HTTP_200_OK)

            # Handle validation errors
            return Response({
                "status": "error",
                "message": "Invalid data provided",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        except models.Product.DoesNotExist:
            return Response({
                "status": "error",
                "message": "Product not found"
            }, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({
                "status": "error",
                "message": f"An error occurred: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CreateCategory(generics.CreateAPIView):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            data = {
                "title": request.data.get("title"),
                "image_url": request.data.get("image_url")
            }

            serializer = self.get_serializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "status": "success",
                    "message": "Category created successfully",
                    "data": serializer.data
                }, status=status.HTTP_201_CREATED)

            return Response({
                "status": "error",
                "message": "Invalid data provided",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                "status": "error",
                "message": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CreateBrand(generics.CreateAPIView):
    queryset = models.Brand.objects.all()
    serializer_class = serializers.BrandSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            data = {
                "title": request.data.get("title"),
                "image_url": request.data.get("image_url")
            }

            serializer = self.get_serializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "status": "success",
                    "message": "Brand created successfully",
                    "data": serializer.data
                }, status=status.HTTP_201_CREATED)

            return Response({
                "status": "error",
                "message": "Invalid data provided",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                "status": "error",
                "message": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DeleteProduct(generics.DestroyAPIView):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete()
            return Response({
                "status": "success",
                "message": "Product deleted successfully"
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "status": "error",
                "message": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DeleteCategory(generics.DestroyAPIView):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete()
            return Response({
                "status": "success",
                "message": "Category deleted successfully"
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "status": "error",
                "message": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DeleteBrand(generics.DestroyAPIView):
    queryset = models.Brand.objects.all()
    serializer_class = serializers.BrandSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete()
            return Response({
                "status": "success",
                "message": "Brand deleted successfully"
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "status": "error",
                "message": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class OrderListCreateView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Get all orders"""
        orders = order_models.Order.objects.all().prefetch_related('items', 'items__product_id').select_related('address')
        
        serializer = order_serializers.OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        """Create a new order"""
        serializer = order_serializers.OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user_id=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderStatusUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        """Update order status"""
        order = get_object_or_404(order_models.Order, pk=pk)
        if not request.user.is_staff:
            return Response(status=status.HTTP_403_FORBIDDEN)

        new_status = request.data.get('status')
        if new_status not in dict(order_models.Order.STATUS_CHOICES):
            return Response(
                {'error': 'Invalid status'},
                status=status.HTTP_400_BAD_REQUEST
            )

        order.status = new_status
        order.save()
        serializer = order_serializers.OrderSerializer(order)
        return Response(serializer.data)

class OrderPaymentStatusUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        """Update payment status"""
        order = get_object_or_404(order_models.Order, pk=pk)
        if not request.user.is_staff:
            return Response(status=status.HTTP_403_FORBIDDEN)

        new_payment_status = request.data.get('payment_status')
        if new_payment_status not in dict(order_models.Order.PAYMENT_STATUS_CHOICES):
            return Response(
                {'error': 'Invalid payment status'},
                status=status.HTTP_400_BAD_REQUEST
            )

        order.payment_status = new_payment_status
        order.save()
        serializer = order_serializers.OrderSerializer(order)
        return Response(serializer.data)

class RecentOrdersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Get recent orders (last 30 days)"""
        thirty_days_ago = datetime.now() - timedelta(days=30)
        if request.user.is_staff:
            orders = order_models.Order.objects.filter(created_at__gte=thirty_days_ago)
        else:
            orders = order_models.Order.objects.filter(
                user_id=request.user,
                created_at__gte=thirty_days_ago
            )
        
        serializer = order_serializers.OrderSerializer(orders, many=True)
        return Response(serializer.data)
