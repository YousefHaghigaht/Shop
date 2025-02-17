from django.shortcuts import render
from django.views import View
from products.models import Product
from django.db import models


class HomePageView(View):

    def get(self,request):
        liked_products = Product.objects.filter(is_available=True).annotate(
            like_count=models.Count('pliked')).order_by('-like_count')[:10]
        popular_products = Product.objects.order_by('-views')
        return render(request,'home/home.html',{
            'liked_products':liked_products,
            'popular_products':popular_products
        })
