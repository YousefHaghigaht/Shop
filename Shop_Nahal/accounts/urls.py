from django.urls import path,include
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = 'accounts'

srz_urls = [
    path('users/',views.UsersListAPIView.as_view(),name='api_users'),
]

urlpatterns = [
    path('register/',views.UserRegisterView.as_view(),name='register'),
    path('login/',views.UserLoginView.as_view(),name='login'),
    path('logout/',views.UserLogoutView.as_view(),name='logout'),
    path('ps/reset/',views.PasswordResetView.as_view(),name='password_reset'),
    path('ps/reset/done/',views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('ps/reset/confirm/<uidb64>/<token>/',views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('pa/reset/complete/',views.PasswordResetComplete.as_view(),name='password_reset_complete'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('',include(srz_urls))
]

