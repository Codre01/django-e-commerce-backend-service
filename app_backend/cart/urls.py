from django.urls import path
from cart import views

urlpatterns = [
    path('me/', views.GetUserCart.as_view(), name='get-cart'),
    path('add/', views.AddItemToCart.as_view(), name='add-to-cart'),
    path('delete/', views.RemoveItemFromCart.as_view(), name='remove-from-cart'),
    path('count/', views.CartCount.as_view(), name='cart-count'),
    path('update/', views.UpdateCartItemQuantity.as_view(), name='update-cart-item'),
]