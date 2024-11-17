from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('detail/<int:product_id>/<slug:product_slug>/',views.ProductDetailView.as_view(),name='detail'),
    path('products_list/',views.ProductsView.as_view(),name='products_list'),
    path('products_list/category/<slug:category_slug>/',views.ProductsView.as_view(),name='category'),
]