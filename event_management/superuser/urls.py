from django.urls import path
from . import views

app_name='superuser'

urlpatterns = [
    path('home', views.home, name='home'),
    path('add_mod',views.add_mod, name='add_mod'),
    path('display',views.display, name='display'),
    path('<int:id>',views.delete,name='delete')
    ]