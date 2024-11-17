from django.urls import path
from . import views


app_name = 'accounts'

urlpatterns = [
    path('register/',views.UserRegistrationView.as_view(),name='register'),
    path('verify_code/',views.UserVerifyCodeView.as_view(),name='verify_code'),
    path('login/',views.UserLoginView.as_view(),name='login'),
    path('logout/',views.UserLogoutView.as_view(),name='logout'),
    path('resend_code/',views.ResendCodeView.as_view(),name='resend_code')
]w