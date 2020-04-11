from django.urls import path
from . import views



urlpatterns = [
    path('signup/', views.SignUp, name='signup'),
    path('signup/additional_info/',views.additional_info,name='additional_info'),
]