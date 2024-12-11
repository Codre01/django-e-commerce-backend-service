from django.urls import path
from order import views

urlpatterns = [
    path('create/', views.AddOrder.as_view(), name='create-order'),
    path('list/me/', views.GetUserOrders.as_view(), name='get-user-orders'),
    path('update/', views.UpdateOrderStatus.as_view(), name='update-order-status'),
    # path('count/', views.CartCount.as_view(), name='cart-count'),
    # path('update/', views.UpdateCartItemQuantity.as_view(), name='update-cart-item'),
]