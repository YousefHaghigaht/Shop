from django.shortcuts import render,redirect
from django.views import View
from .forms import VerifyCodeForm,UserRegistrationForm,UserLoginForm
import random
from .models import OtpCode,User
from django.contrib import messages
from utils import send_otp_code
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime,timedelta
import pytz


class UserRegistrationView(View):
    """
     Users registration class
    """
    form_class = UserRegistrationForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.error(request,'You are in your account.')
            return redirect('home:home')
        return super().dispatch(request,*args,**kwargs)

    def get(self,request):
        form = self.form_class
        return render(request,'accounts/register.html',{'form':form})

    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            request.session['user_registration_info'] = {
                'phone_number': cd['phone_number'],
                'email': cd['email'],
                'full_name': cd['full_name'],
                'password': cd['password1']
            }
            random_code = random.randint(1000,9999)
            otp_exist = OtpCode.objects.filter(phone_number=cd['phone_number'])
            if otp_exist.exists():
                otp_exist.delete()
            otp = OtpCode.objects.create(phone_number=cd['phone_number'],code=random_code)
            send_otp_code(phone_number=cd['phone_number'],code=random_code)
            print(otp.code)
            print(otp.created)
            messages.success(request,'We sent a code to your phone','success')
            return redirect('accounts:verify_code')


class UserVerifyCodeView(View):
    """
    User registration with arguments of
     'phone number, email, full name, password'
    """
    form_class = VerifyCodeForm

    def dispatch(self, request, *args, **kwargs):
        # Check if the user is not logged in

        if request.user.is_authenticated:
            messages.error(request,'You are in your account.')
            return redirect('home:home')
        return super().dispatch(request,*args,**kwargs)

    def setup(self, request, *args, **kwargs):
        self.user_session = request.session['user_registration_info']
        self.code_instance = OtpCode.objects.get(phone_number=self.user_session['phone_number'])
        return super().setup(request,*args,**kwargs)

    def get(self,request):
        form = self.form_class
        enable_btn = False
        expire_time = datetime.now(tz=pytz.timezone('Asia/Tehran')) - timedelta(minutes=1)
        if self.code_instance.created > expire_time:
            enable_btn = True
        print(expire_time)
        print(self.code_instance.created)
        return render(request,'accounts/verify_code.html',{'form':form,'enable_btn':enable_btn})

    def post(self,request):
        form = self.form_class(request.POST)
        user_session = self.user_session
        code_instance = self.code_instance
        expire_time = datetime.now(tz=pytz.timezone('Asia/Tehran')) - timedelta(minutes=1)
        if form.is_valid():
            if form.cleaned_data['code'] == code_instance.code and code_instance.created > expire_time :
                User.objects.create_user(
                    phone_number= user_session['phone_number'],
                    email= user_session['email'],
                    full_name= user_session['full_name'],
                    password= user_session['password']
                )
                code_instance.delete()
                messages.success(request,'You have successfully registered','success')
                return redirect('home:home')
            elif code_instance.created < expire_time:
                messages.error(request,'The entered code has expired','danger')
            else:
                messages.error(request,'The entered code is not correct','danger')
            return redirect('accounts:verify_code')


class UserLoginView(View):
    form_class = UserLoginForm
    """
    User login with 'phone number' and 'password'
    """

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.error(request,'You are in your account.')
            return redirect('home:home')
        return super().dispatch(request,*args,**kwargs)

    def get(self,request):
        form = self.form_class
        return render(request,'accounts/login.html',{'form':form})

    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(phone_number=cd['phone_number'],password=cd['password'])
            if user:
                login(request,user)
                messages.success(request,'You are logged into your account','success')
                return redirect('home:home')
            else:
                messages.error(request,'The phone number does not match the password','danger')
                return redirect('accounts:login')


class ResendCodeView(View):

    """
    Resend the code if the previous code expires
    """

    def get(self,request):
        user_session = request.session['user_registration_info']
        expire_time = datetime.now(tz=pytz.timezone('Asia/Tehran')) - timedelta(minutes=1)
        code_instance = OtpCode.objects.get(phone_number=user_session['phone_number'])
        if code_instance.created < expire_time:
            code_instance.delete()
            random_code = random.randint(1000,9999)
            otp = OtpCode.objects.create(phone_number=user_session['phone_number'],code=random_code)
            print(otp.code)
            messages.success(request,'We resent a new code to your phone.','success')
            return redirect('accounts:verify_code')
        messages.error(request,'Your code is not expire.','danger')
        return redirect('accounts:verify_code')


class UserLogoutView(LoginRequiredMixin,View):
    """
    User logout
    """

    def get(self,request):
        logout(request)
        messages.success(request,'You are logged out of your account.','success')
        return redirect('home:home')








