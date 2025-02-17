from django.shortcuts import get_object_or_404,render,redirect
from django.views.generic import DetailView
from .models import Product,Vote,Category
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from orders.forms import QuantityForm

# API
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CategoriesSerializer,ProductsSerializer,VotesSerializer


class ProductListView(View):

    """
    List all products with product categories
    By selecting any category, related products will be shown
    """

    def get(self,request,category_slug=None):
        products = Product.objects.filter(is_available=True)
        categories = Category.objects.filter(is_sub=False)
        if category_slug:
            category = get_object_or_404(Category,slug=category_slug)
            products = Product.objects.filter(category=category)
        return render(request,'products/products_list.html',{
            'products':products,
            'categories':categories,})


class ProductDetailView(DetailView):
    """
    Show a product detail

    Add a comment on a product
    Ajax  management by django-comments-dab

    """

    def get(self,request,*args,**kwargs):
        product = get_object_or_404(Product,id=kwargs['product_id'],slug=kwargs['product_slug'])
        form = QuantityForm
        return render(request,'products/detail.html',{'product':product,
                                                      'form':form,})


class ProductLikeView(LoginRequiredMixin,View):
    """
    Liking a product
    If you have already liked, you will encounter an error
    """

    def get(self,request,product_id):
        product = get_object_or_404(Product,id=product_id)
        vote = Vote.objects.filter(user=request.user,product=product).exists()
        if vote:
            messages.error(request,'You liked already this product','danger')
        else:
            Vote.objects.create(user=request.user,product=product)
        return redirect('products:detail',product.id,product.slug)


# fields API serializer
class CategoriesListAPIView(APIView):
    """
    List of all product categories
    """
    serializer_class = CategoriesSerializer

    def get(self,request):
        categories = Category.objects.all()
        srz_data = self.serializer_class(instance=categories,many=True)
        return Response(srz_data.data,status=status.HTTP_200_OK)


class ProductsListAPIView(APIView):
    """
    Serialization of product fields
    """
    serializer_class = ProductsSerializer

    def get(self,request):
        products = Product.objects.all()
        srz_data = self.serializer_class(instance=products,many=True)
        return Response(srz_data.data,status=status.HTTP_200_OK)


class VotesListAPIView(APIView):
    """
    Serialization of vote fields
    """
    serializer_class = VotesSerializer

    def get(self,request):
        votes = Vote.objects.all()
        srz_data = self.serializer_class(instance=votes,many=True)
        return Response(srz_data.data,status=status.HTTP_200_OK)


