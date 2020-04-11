from django.contrib import admin
from django.urls import path, include
from . import views

app_name=  'event'
urlpatterns = [
    path('<str:eventid>',views.eventdetails,name='eventdetails'),
    path('<str:regeventid>/registerevent',views.eventregister,name='eventregister'),
    path('<str:dropeventid>/dropevent',views.eventdropout,name='eventdropout'),
    path('<str:eventid>/changedetails',views.changedetails,name='changedetails')
]
