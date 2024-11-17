from django.urls import path,include
from . import views

app_name = 'products'

srz_data = [
    path('categories/',views.CategoriesListAPIView.as_view(),name='categories_list'),
    path('products_list/',views.ProductsListAPIView.as_view(),name='products_list_api'),
    path('votes/',views.VotesListAPIView.as_view(),name='votes_list'),
]

urlpatterns = [
    path('list/',views.ProductListView.as_view(),name='products_list'),
    path('category/<slug:category_slug>/',views.ProductListView.as_view(),name='category'),
    path('detail/<int:product_id>/<slug:product_slug>/',views.ProductDetailView.as_view(),name='detail'),
    path('like/<int:product_id>/',views.ProductLikeView.as_view(),name='like'),
    path('',include(srz_data))
]