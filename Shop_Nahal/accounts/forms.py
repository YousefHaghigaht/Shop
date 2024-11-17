from django import forms
from .models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.forms import PasswordResetForm,SetPasswordForm


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password',widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation',widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('phone_number','email','full_name','password1','password2')

    # Style form
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class':'form-control'})

    # Matching passwords
    def clean_password2(self):
        p1 = self.cleaned_data['password1']
        p2 = self.cleaned_data['password2']
        if p1 and p2 and p1 != p2:
            raise ValidationError('Passwords dont match')
        return p2

    def save(self,commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(help_text='Click <a href=\'../password\'>this link</a> to change the password.')

    class Meta:
        model = User
        fields = ('phone_number','email','full_name','password','is_active','is_admin','last_login')


class UserLoginForm(forms.Form):
    phone_number = forms.CharField(label='Phone number',widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label='Email',widget=forms.EmailInput(attrs={'class':'form-control'}))


class CustomSetPasswordResetForm(SetPasswordForm):

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class':'form-control'})
