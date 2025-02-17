from django.shortcuts import render,get_object_or_404
from django.views.generic import DetailView,ListView
from .models import Product,Category
from django.views import View
from .forms import QuantityForm


class ProductDetailView(DetailView):
    template_name = 'products/detail.html'
    context_object_name = 'product'
    form_class = QuantityForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class
        return context

    def get_object(self, queryset=None):
        return get_object_or_404(Product,id=self.kwargs['product_id'],slug=self.kwargs['product_slug'])


class ProductsView(View):

    def get(self,request, category_slug=None):
        products = Product.objects.filter(is_available=True)
        categories = Category.objects.filter(is_sub=False)
        if category_slug:
            category = get_object_or_404(Category,slug=category_slug)
            products = Product.objects.filter(category=category)
        return render(request,'products/products_list.html',{'products':products,'categories':categories})