from django.urls import path
from . import views

app_name = 'about'

urlpatterns = [
    path('us/',views.AboutUsView.as_view(),name='about_us'),
    path('contact/',views.CantactUsView.as_view(),name='contact_us'),
]
