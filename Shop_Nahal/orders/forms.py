from django import forms


class QuantityForm(forms.Form):
    quantity = forms.IntegerField(label='Quantity')


class CouponForm(forms.Form):
    code = forms.CharField(label='Discount code')


