from django.contrib import admin
from django.urls import path, include
from auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path("auth/logout/", LogoutView.as_view()),
    
    path('api/products/', include('core.urls')),
    path('api/wishlist/', include('wishlist.urls')),
    path('api/cart/', include('cart.urls')),
    path('api/address/', include('checkout.urls')),
    path('api/order/', include('order.urls')),
    path('api/admin/', include('admins.urls')),
]
