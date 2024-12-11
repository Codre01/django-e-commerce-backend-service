from django.contrib import admin
from django.urls import path, include
from core import views

urlpatterns = [
    path('categories/', views.CategoryList.as_view(), name='category-list'),
    path('brands/', views.BrandList.as_view(), name='brand-list'),
    path('categories/home/', views.HomeCategoryList.as_view(), name='home-category-list'),
    
    path('', views.ProductList.as_view(), name='product-list'),
    path('byType/', views.ProductListByClothesType.as_view(), name='list-by-type'),
    path('popular/', views.PopularProductsList.as_view(), name='popular-product-list'),
    path('search/', views.SearchProductByTitle.as_view(), name='search'),
    path('category/', views.FilterProductByCategory.as_view(), name='products-by-category'),
    path('recommendations/', views.SimilarProducts.as_view(), name='similar-products'),
    
]