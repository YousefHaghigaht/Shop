from rest_framework import serializers
from .models import Order,OrderItem,Coupon


class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class CouponsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = '__all__'


