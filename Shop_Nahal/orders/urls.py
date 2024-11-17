from django.urls import path,include
from . import views

app_name = 'orders'

srz_urls = [
    path('list/',views.OrdersListAPIViews.as_view(),name='orders_list'),
    path('items_list/',views.OrderItemsAPIViews.as_view(),name='order_items'),
    path('coupon_list/',views.CouponListAPIView.as_view(),name='coupon_list')
]

urlpatterns = [
    path('cart/',views.CartView.as_view(),name='cart'),
    path('cart/create/<int:post_id>/',views.CartAddView.as_view(),name='add_to_cart'),
    path('create/',views.OrderCreateView.as_view(),name='create'),
    path('detail/<int:order_id>/',views.OrderDetailView.as_view(),name='detail'),
    path('order_pay/<int:order_id>/', views.OrderPayView.as_view(), name='order_pay'),
    path('verify/', views.OrderVerify.as_view(), name='verify'),
    path('',include(srz_urls)),
]