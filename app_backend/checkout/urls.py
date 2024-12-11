from django.urls import path
from checkout import views

urlpatterns = [
    path('addresslist/', views.GetUserAddresses.as_view(), name='user-addresses'),
    path('add/', views.AddAddress.as_view(), name='add-address'),
    path('delete/', views.DeleteAddress.as_view(), name='delete-address'),
    path('default/', views.SetDefaultAddress.as_view(), name='set-default-address'),
    path('me/', views.GetDefaultAddress.as_view(), name='get-default-address'),
]