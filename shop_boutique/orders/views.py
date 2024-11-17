from django.shortcuts import render,get_object_or_404,redirect
from django.views import View
from .cart import Cart
from products.forms import QuantityForm
from products.models import Product
from django.contrib import messages
from .models import Order,OrderItem,Coupon
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CouponForm
from datetime import datetime
import pytz
import requests
from django.conf import settings
import json


class CartView(View):

    def get(self,request):
        products = Cart(request)
        return render(request,'orders/cart.html',{'products':products})


class AddCartView(View):

    def post(self,request,product_id):
        cart = Cart(request)
        product = get_object_or_404(Product,id=product_id)
        form = QuantityForm(request.POST)
        if form.is_valid():
            cart.add(form.cleaned_data['quantity'],product)
            messages.success(request,'The product added to cart.','success')
            return redirect('orders:cart')


class RemoveProductCartView(View):

    def get(self,request,product_id):
        cart = Cart(request)
        product = get_object_or_404(Product,id=product_id)
        cart.remove(product)
        messages.success(request,'The product deleted from your cart','success')
        return redirect('orders:cart')


class OrderCreateView(LoginRequiredMixin,View):

    def get(self,request):
        cart = Cart(request)
        order = Order.objects.create(user=request.user)
        for item in cart:
            OrderItem.objects.create(order=order,product=item['product'],price=item['price'],quantity=item['quantity'])
        return redirect('orders:detail',order.id)


class OrderDetailView(LoginRequiredMixin,View):
    form_class = CouponForm

    def get(self,request,order_id):
        cart = Cart(request)
        order = get_object_or_404(Order,id=order_id)
        return render(request, 'orders/checkout.html', {
            'order':order,'cart':cart,'form':self.form_class
        })

    def post(self,request,*args,**kwargs):
        order = get_object_or_404(Order,id=kwargs['order_id'])
        form = self.form_class(request.POST)
        now = datetime.now(tz=pytz.timezone('Asia/Tehran'))
        if form.is_valid():
            try:
                coupon = Coupon.objects.get(code__exact=form.cleaned_data['code'],valid_from__lte=now,
                                   valid_to__gte=now,is_active=True)
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
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
phone = 'YOUR_PHONE_NUMBER'  # Optional
# Important: need to edit for realy server.
CallbackURL = 'http://127.0.0.1:8000/verify/'


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


