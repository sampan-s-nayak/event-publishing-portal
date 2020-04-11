from django.urls import path, include
from django.views.generic.base import TemplateView
from . import views

urlpatterns = [
	path('',views.search, name='search')  
]
