from django import forms


class QuantityForm(forms.Form):
    quantity = forms.IntegerField(min_value=0,widget=forms.NumberInput(attrs={'class':'form-control'}))