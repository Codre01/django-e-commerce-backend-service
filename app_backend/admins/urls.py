from django.urls import path
from . import views

urlpatterns = [
    path('products/list/', views.ProductList.as_view(), name='get-products-list'),
    path('products/create/', views.CreateProduct.as_view(), name='create-product'),
    path('products/update/<int:id>/', views.UpdateProduct.as_view(), name='update-product'),
    path('products/delete/<int:id>/', views.DeleteProduct.as_view(), name='delete-product'),
    path('categories/create/', views.CreateCategory.as_view(), name='create-category'),
    path('categories/delete/<int:id>/', views.DeleteCategory.as_view(), name='delete-category'),
    path('brands/create/', views.CreateBrand.as_view(), name='create-brand'),
    path('brands/delete/<int:id>/', views.DeleteBrand.as_view(), name='delete-brand'),
    path('orders/', views.OrderListCreateView.as_view(), name='order-list-create'),
    path('orders/<int:pk>/update-status/', views.OrderStatusUpdateView.as_view(), name='order-status-update'),
    path('orders/<int:pk>/update-payment-status/', views.OrderPaymentStatusUpdateView.as_view(), name='order-payment-status-update'),
    path('orders/recent/', views.RecentOrdersView.as_view(),  name='recent-orders'),
]