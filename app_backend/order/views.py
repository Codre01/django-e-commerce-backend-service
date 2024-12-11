from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db import transaction
from . import models, serializers
from checkout.models import Address


class AddOrder(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        required_fields = ['address_id', 'items']

        for field in required_fields:
            if field not in data:
                return Response({'message': f'{field} is required'}, status=status.HTTP_400_BAD_REQUEST)

        if not isinstance(data['items'], list) or len(data['items']) == 0:
            return Response({'message': 'Items must be a non-empty list'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = request.user
            address = get_object_or_404(Address, id=data['address_id'], user_id=user.id)
            total_amount = 0

            with transaction.atomic():
                order = models.Order.objects.create(
                    user_id=user,
                    address=address,
                    total_amount=0,
                    status='pending',
                    payment_status='pending'
                )

                for item in data['items']:
                    product = get_object_or_404(models.Product, id=item.get('product_id'))
                    quantity = item.get('quantity', 0)

                    if quantity <= 0:
                        raise ValueError('Quantity must be greater than zero')

                    size = item.get('size', 'default')
                    color = item.get('color', 'default')

                    models.OrderItem.objects.create(
                        order_id=order,
                        product_id=product,
                        quantity=quantity,
                        price=product.price,
                        size=size,
                        color=color
                    )
                    total_amount += product.price * quantity
                    product.save()

                order.total_amount = total_amount
                order.save()

            return Response({'message': 'Order added successfully'}, status=status.HTTP_201_CREATED)
        except models.Product.DoesNotExist:
            return Response({'message': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        except ValueError as ve:
            return Response({'message': str(ve)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetUserOrders(generics.ListAPIView):
    serializer_class = serializers.OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return models.Order.objects.filter(user_id=self.request.user).prefetch_related(
            'items', 
            'items__product_id'
        ).select_related('address')

class UpdateOrderStatus(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        order_id = request.query_params.get('id')
        status = request.data.get('status')

        if not order_id or not status:
            return Response({'message': 'Order id and status are required'}, status=status.HTTP_400_BAD_REQUEST)

        valid_statuses = ['pending', 'in_progress', 'completed', 'cancelled']
        if status not in valid_statuses:
            return Response({'message': f'Invalid status. Valid statuses are: {", ".join(valid_statuses)}'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            order = models.Order.objects.get(id=order_id, user_id=request.user)

            if order.status in ['completed', 'cancelled']:
                return Response({'message': f'Cannot update status of {order.status} orders'}, status=status.HTTP_400_BAD_REQUEST)

            order.status = status
            order.save()
            return Response({'message': 'Order status updated successfully'}, status=status.HTTP_200_OK)
        except models.Order.DoesNotExist:
            return Response({'message': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

   
