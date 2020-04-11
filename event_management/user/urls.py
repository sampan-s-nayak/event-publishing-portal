from django.urls import path
from . import views

app_name='users'

urlpatterns = [
    path('create_event', views.create_event, name='create_event'),
    path('display_events',views.display_events, name='display_events'),
    path('add_event', views.add_event, name='add_event'),
    path('hosted_events',views.hosted_events, name='hosted_events'),
    path('report_user/<int:id>/',views.report_user,name='report_user'),
    path('createdevents',views.createdevents,name='createdevents'),
    path('joinedevents',views.joinedevents,name='joinedevents'),
    path('<int:eventid>/getregistrations',views.getregistrations,name='getregistrations'),
    path('dashboard',views.dashboard,name='dashboard')
    ]