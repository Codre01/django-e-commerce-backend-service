from django.urls import path
from wishlist import views

urlpatterns = [
    path('', views.GetWishList.as_view(), name='get-wishlist'),
    path('toggle/', views.ToggleWishList.as_view(), name='add-remove-wishlist'),
]