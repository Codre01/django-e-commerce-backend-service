from rest_framework import generics, status
from . import models, serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count
from rest_framework.permissions import AllowAny
import random

class CategoryList(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    
class BrandList(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = models.Brand.objects.all()
    serializer_class = serializers.BrandSerializer

# To randomize the products on the home screen
class HomeCategoryList(generics.ListAPIView):
    serializer_class = serializers.CategorySerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = models.Category.objects.all()
        queryset = queryset.annotate(product_count=Count('id'))
        queryset = list(queryset)
        random.shuffle(queryset)
        return queryset[:5]
    
class BrandList(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = models.Brand.objects.all()
    serializer_class = serializers.BrandSerializer
    
    
class ProductList(generics.ListAPIView):
    serializer_class = serializers.ProductSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = models.Product.objects.all()
        queryset = queryset.annotate(product_count=Count('id'))
        queryset = list(queryset)
        random.shuffle(queryset)
        return queryset[:20]
    
class PopularProductsList(generics.ListAPIView):
    serializer_class = serializers.ProductSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = models.Product.objects.filter(rating__gte=4.0, rating__lte=5.0)
        queryset = queryset.annotate(product_count=Count('id'))
        queryset = list(queryset)
        random.shuffle(queryset)
        return queryset[:20]
    
class ProductListByClothesType(APIView):
    serializer_class = serializers.ProductSerializer
    permission_classes = [AllowAny]

    def get(self, request):
        query = request.query_params.get("clothesType", None)
        if query:
            queryset = models.Product.objects.filter(clothes_type=query)
            queryset = queryset.annotate(random_order=Count('id'))
            product_list = list(queryset)
            random.shuffle(product_list)
            
            limited_products = product_list[:20]
            serializer = serializers.ProductSerializer(limited_products, many=True)
            return Response(serializer.data)
        else:
            return Response({'message': 'No query Provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        
class SimilarProducts(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        query = request.query_params.get("category", None)
        
        if(query):
            products = models.Product.objects.filter(category=query)
            product_list = list(products)
            random.shuffle(product_list)
            
            limited_products = product_list[:6]
            serializer = serializers.ProductSerializer(limited_products, many=True)
            return Response(serializer.data)
        else:
            return Response({'message': 'No query Provided'}, status=status.HTTP_400_BAD_REQUEST)

class SearchProductByTitle(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        query = request.query_params.get("q", None)
        
        if query:
            products = models.Product.objects.filter(title__icontains=query)
            
            serializer = serializers.ProductSerializer(products, many=True)
            return Response(serializer.data)
        else:
            return Response({'message': 'No query Provided'}, status=status.HTTP_400_BAD_REQUEST)
        
class FilterProductByCategory(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        query = request.query_params.get("category", None)
        
        if query:
            products = models.Product.objects.filter(category=query)
            
            serializer = serializers.ProductSerializer(products, many=True)
            return Response(serializer.data)
        else:
            return Response({'message': 'No query Provided'}, status=status.HTTP_400_BAD_REQUEST)