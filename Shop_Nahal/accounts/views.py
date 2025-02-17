from django.shortcuts import render,redirect
from django.views import View
from .forms import UserCreationForm,UserLoginForm,CustomPasswordResetForm,CustomSetPasswordResetForm
from .models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout,views as auth_view
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

# API
from rest_framework.views import APIView
from .serializers import UsersSerializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser


class UserRegisterView(View):
    """
    User registration with phone number, email, full name, password, confirm password fields
    """
    form_class = UserCreationForm

    # Checking the logged in user and rejecting it
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request,*args,**kwargs)

    def get(self,request):
        form = self.form_class
        return render(request,'accounts/register.html',{'form':form})

    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(
                phone_number=cd['phone_number'],
                email=cd['email'],
                full_name=cd['full_name'],
                password=cd['password1']
            )
            messages.success(request,'You have successfully registered','success')
            return redirect('home:home')


class UserLoginView(View):
    """
    User login with phone number and password fields
    """
    form_class = UserLoginForm

    # Checking the logged in user and rejecting it
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request,*args,**kwargs)

    def get(self,request):
        form = self.form_class
        return render(request,'accounts/login.html',{'form':form})

    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,username=cd['phone_number'],password=cd['password'])
            if user:
                login(request,user)
                messages.success(request,'You have successfully logged in.','success')
                return redirect('home:home')
            messages.error(request,'The phone number does not match the password','danger')
            return redirect('accounts:login')


class UserLogoutView(LoginRequiredMixin,View):
    """
    User logout
    """
    def get(self,request):
        logout(request)
        messages.success(request,'You have successfully logged out','success')
        return redirect('home:home')


class PasswordResetView(auth_view.PasswordResetView):
    """
    Show email input form and send email text
    """
    template_name = 'accounts/password_reset_form.html'
    email_template_name = 'accounts/password_reset_email.html'
    form_class = CustomPasswordResetForm
    success_url = reverse_lazy('accounts:password_reset_done')


class PasswordResetDoneView(auth_view.PasswordResetDoneView):
    """
    Show success message
    """
    template_name = 'accounts/password_reset_done.html'


class PasswordResetConfirmView(auth_view.PasswordResetConfirmView):
    """
    Enter new password
    with password, confirm password fields
    """
    template_name = 'accounts/password_reset_confirm.html'
    form_class = CustomSetPasswordResetForm
    success_url = reverse_lazy('accounts:password_reset_complete')


class PasswordResetComplete(auth_view.PasswordResetCompleteView):
    """Show success message"""

    template_name = 'accounts/password_reset_complete.html'


# API fields serializer
class UsersListAPIView(APIView):
    """
    List users
    Provided that the requesting user is an admin
    """
    serializer_class = UsersSerializers
    permission_classes = [IsAdminUser]

    def get(self,request):
        users = User.objects.all()
        srz_users = self.serializer_class(inspect=users,many=True)
        return Response(data=srz_users.data,status=status.HTTP_200_OK)







