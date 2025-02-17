from django.shortcuts import render
from django.views.generic import ListView
from products.models import Product,Category


class HomePageView(ListView):
    queryset = Product.objects.filter(is_available=True)
    template_name = 'home/home.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(is_sub=False)
        return context

