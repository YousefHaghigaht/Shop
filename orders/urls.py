from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('create/',views.OrderCreateView.as_view(),name='create'),
    path('detail/<int:order_id>/',views.OrderDetailView.as_view(),name='detail'),
    path('cart/',views.CartView.as_view(),name='cart'),
    path('add_cart/<int:product_id>/',views.AddCartView.as_view(),name='add_to_cart'),
    path('remove/<int:product_id>/',views.RemoveProductCartView.as_view(),name='remove_product')
]