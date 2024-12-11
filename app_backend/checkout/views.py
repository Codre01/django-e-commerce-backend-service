from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from . import models, serializers
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db import transaction

# Create your views here.
class AddAddress(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        data = request.data
        
        user_address = models.Address.objects.create(
            user_id=request.user,
            is_default = data['is_default'],
            address = data['address'],
            phone = data['phone'],
            address_type = data['address_type']
        )
        
        if user_address.is_default:
            models.Address.objects.filter(user_id=request.user).update(is_default=False)
            
        user_address.save()
        
        return Response({'message': 'Address added successfully'}, status=status.HTTP_201_CREATED)
    
    
class GetUserAddresses(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        addresses =models.Address.objects.filter(user_id=request.user)
        serializer = serializers.AddressSerializer(addresses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class GetDefaultAddress(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        address = models.Address.objects.filter(user_id=request.user, is_default=True)

        if address.exists():
            address_serializer = serializers.AddressSerializer(address.first())
            return Response(address_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'No default address found'}, status=status.HTTP_404_NOT_FOUND)

        
class DeleteAddress(APIView):
    permission_classes = [IsAuthenticated]
    
    def delete(self, request):
        address_id = request.query_params.get('id')
        
        if not address_id:
            return Response({'message': 'Address id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = request.user
            address_item = models.Address.objects.get(user_id=user, id=address_id)
            with transaction.atomic():
                if address_item.is_default:
                    other_address = models.Address.objects.filter(user_id=user).exclude(id=address_id)
                    
                    if other_address.exists():
                        new_default_address = other_address.first()
                        new_default_address.is_default = True
                        new_default_address.save()
                    else:
                        return Response({'message': 'You can not delete a default address without any other address.'}, status=status.HTTP_400_BAD_REQUEST)
                    
                address_item.delete()
                
                return Response({'message': 'Address deleted successfully'}, status=status.HTTP_200_OK)
        except models.Address.DoesNotExist:
            return Response({'message': 'Address not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class SetDefaultAddress(APIView):
    permission_classes = [IsAuthenticated]
    
    def patch(self, request):
        address_id = request.query_params.get('id')
        
        if not address_id:
            return Response({'message': 'Address id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = request.user
            address_item = models.Address.objects.get(id=address_id)
            
            models.Address.objects.filter(user_id=user).update(is_default=False)
            
            address_item.is_default = True
            address_item.save()
            
            return Response({'message': 'Address set as default'}, status=status.HTTP_200_OK)
        except models.Address.DoesNotExist:
            return Response({'message': 'Address not found'}, status=status.HTTP_404_NOT_FOUND)
            
        