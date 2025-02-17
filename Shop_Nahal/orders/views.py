from django.shortcuts import render,get_object_or_404,redirect
from django.views import View
from .cart import Cart
from products.models import Product
from .forms import QuantityForm,CouponForm
from django.contrib import messages
from .models import Order,OrderItem,Coupon
from datetime import datetime
import pytz
import requests
from django.conf import settings
import json
from django.contrib.auth.mixins import LoginRequiredMixin

# API
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import OrdersSerializer,OrderItemSerializer,CouponsSerializer
from rest_framework.permissions import IsAdminUser


class CartView(LoginRequiredMixin,View):
    """
    Show shopping cart
    Specifications:
    Product name and photo,
    Price and number of products,
    Total price
    """

    def get(self,request):
        products = Cart(request)
        return render(request,'orders/cart.html',{'products':products})


class CartAddView(LoginRequiredMixin,View):
    """
    Add a product on cart
    Send the product and its quantity to the shopping cart
    """

    def post(self,request,post_id):
        cart = Cart(request)
        product = get_object_or_404(Product,id=post_id)
        form = QuantityForm(request.POST)
        if form.is_valid():
            cart.add(form.cleaned_data['quantity'],product)
            messages.success(request,'The product added to cart','success')
            return redirect('orders:cart')


class OrderCreateView(LoginRequiredMixin,View):
    """
    Creating an order after hitting the checkout button in the shopping cart
    and directing the user to the order details page
    """

    def get(self,request):
        cart = Cart(request)
        order = Order.objects.create(user=request.user)
        for item in cart:
            OrderItem.objects.create(order=order,product=item['product'],quantity=item['quantity'],price=item['price'])
        cart.delete()
        return redirect('orders:detail',order.id)


class OrderDetailView(LoginRequiredMixin,View):
    """
    Showing the details of an order and the form to receive a discount code and calculate it.
    """
    form_class = CouponForm

    def get(self,request,*args,**kwargs):
        cart = Cart(request)
        order = get_object_or_404(Order,id=kwargs['order_id'])
        form = self.form_class
        return render(request,'orders/checkout.html',{'order':order,'form':form,'cart':cart})

    def post(self,request,*args,**kwargs):
        form = self.form_class(request.POST)
        order = get_object_or_404(Order,id=kwargs['order_id'])
        now = datetime.now(tz=pytz.timezone('Asia/Tehran'))
        if form.is_valid():
            try:
                coupon = Coupon.objects.get(code__exact=form.cleaned_data['code'],
                                   from_valid__lte=now,to_valid__gte=now,is_active=True)
            except Coupon.DoesNotExist:
                messages.error(request,'The entered code is not correct','danger')
                return redirect('orders:detail',order.id)
            order.discount = coupon.discount
            order.save()
            messages.success(request,'The entered code has been applied','success')
            return redirect('orders:detail',order.id)


# ZarinPal settings
if settings.SANDBOX:
    sandbox = 'sandbox'
else:
    sandbox = 'www'

ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"

amount = 1000  # Rial / Required
description = "Description"  # Required
phone = 'YOUR_PHONE_NUMBER'  # Optional
# Important: need to edit for realy server.
CallbackURL = 'http://127.0.0.1:8080/verify/'


class OrderPayView(View):

    def get(self,request,order_id):
        order = get_object_or_404(Order,id=order_id)
        request.session['order_pay'] = {
            'order_id':order.id,
        }
        data = {
            "MerchantID": settings.MERCHANT,
            "Amount": order.get_total_price(),
            "Description": description,
            "Phone": phone,
            "CallbackURL": CallbackURL,
        }
        data = json.dumps(data)
        # set content length by data
        headers = {'content-type': 'application/json', 'content-length': str(len(data))}
        try:
            response = requests.post(ZP_API_REQUEST, data=data, headers=headers, timeout=10)

            if response.status_code == 200:
                response = response.json()
                if response['Status'] == 100:
                    return {'status': True, 'url': ZP_API_STARTPAY + str(response['Authority']),
                            'authority': response['Authority']}
                else:
                    return {'status': False, 'code': str(response['Status'])}
            return response

        except requests.exceptions.Timeout:
            return {'status': False, 'code': 'timeout'}
        except requests.exceptions.ConnectionError:
            return {'status': False, 'code': 'connection error'}


class OrderVerify(View):

    def get(self,request,authority):
        order_id = request.session['order_pay']['order_id']
        order = get_object_or_404(Order,id=order_id)
        data = {
            "MerchantID": settings.MERCHANT,
            "Amount": order.get_total_price(),
            "Authority": authority,
        }
        data = json.dumps(data)
        # set content length by data
        headers = {'content-type': 'application/json', 'content-length': str(len(data))}
        response = requests.post(ZP_API_VERIFY, data=data, headers=headers)

        if response.status_code == 200:
            response = response.json()
            if response['Status'] == 100:
                return {'status': True, 'RefID': response['RefID']}
            else:
                return {'status': False, 'code': str(response['Status'])}
        return response


# fields API serializer
class OrdersListAPIViews(APIView):
    """
    List of all orders
    For the requesting admin
    """
    serializer_class = OrdersSerializer

    def get(self,request):
        orders = Order.objects.all()
        srz_data = self.serializer_class(instance=orders,many=True)
        return Response(data=srz_data.data,status=status.HTTP_200_OK)


class OrderItemsAPIViews(APIView):
    """
    List of all ordered products
    """
    serializer_class = OrderItemSerializer

    def get(self,request):
        items = OrderItem.objects.all()
        srz_data = OrderItemSerializer(instance=items,many=True)
        return Response(srz_data.data,status=status.HTTP_200_OK)


class CouponListAPIView(APIView):
    """
    List of all discount codes with details
    For the requesting administrator user
    """
    serializer_class = CouponsSerializer
    permission_classes = [IsAdminUser]

    def get(self,request):
        coupons = Coupon.objects.all()
        srz_data = self.serializer_class(instance=coupons,many=True)
        return Response(srz_data.data,status=status.HTTP_200_OK)








