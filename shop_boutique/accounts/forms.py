from django import forms
from .models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class UserCreationForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """
    password1 = forms.CharField(label='Password',widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation',widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('phone_number','email','full_name','password1','password2')

    def clean_phone_number(self):
        # Check phone number
        phone_number = self.cleaned_data['phone_number']
        user = User.objects.filter(phone_number=phone_number).exists()
        if user:
            raise ValidationError('The entered phone number already exist.')
        return phone_number

    def clean_password2(self):
        # Check that the two password entries match
        p1 = self.cleaned_data['password1']
        p2 = self.cleaned_data['password2']
        if p1 and p2 and p1 != p2:
            raise ValidationError('Passwords dont match!')
        return p2

    def save(self,commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(help_text='Click <a href=\'../password\'>this link</a> to change the password.')

    class Meta:
        model = User
        fields = ('phone_number','email','full_name','password','is_active','is_admin')


class UserRegistrationForm(forms.Form):
    phone_number = forms.CharField(label='Phone number',widget=forms.TextInput(
        attrs={'class':'form-control','placeholder':'Phone number'}))
    email = forms.EmailField(label='Email',widget=forms.EmailInput(
        attrs={'class':'form-control','placeholder':'Email'}))
    full_name = forms.CharField(label='Full name',widget=forms.TextInput(
        attrs={'class':'form-control','placeholder':'Full name'}))
    password1 = forms.CharField(label='Password',widget=forms.PasswordInput(
        attrs={'class':'form-control','placeholder':'Password'}
    ))
    password2 = forms.CharField(label='Password Confirmation',widget=forms.PasswordInput(
        attrs={'class':'form-control','placeholder':'Password confirmation'}
    ))

    def clean(self):
        cd = super().clean()
        p1 = cd.get(self.cleaned_data['password1'])
        p2 = cd.get(self.cleaned_data['password2'])
        if p1 and p2 and p1 != p2:
            raise ValidationError('Passwords dont match')
        return cd

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        user = User.objects.filter(phone_number=phone_number).exists()
        if user:
            raise ValidationError('The entered phone_number already exist')
        return phone_number


class VerifyCodeForm(forms.Form):
    code = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control','placeholder':'****'}))


class UserLoginForm(forms.Form):
    phone_number = forms.CharField(label='Phone number',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Phone number'}))
    password = forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}))


