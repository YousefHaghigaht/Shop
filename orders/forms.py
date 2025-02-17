from django import forms


class CouponForm(forms.Form):
    code = forms.CharField(label='Code Discount',widget=forms.TextInput(attrs={'class':'form-control'}))
