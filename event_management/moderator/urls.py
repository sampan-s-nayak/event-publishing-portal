from django.urls import path
from . import views

app_name='moderator'

urlpatterns = [
    path('black_list/<int:id>/<int:duration>/',views.blacklist_user,name='blacklist'),
    path('view_reported_users/',views.view_reported_users,name='view_reported_users'),
	path('<int:eventid>/<str:decision>/action',views.action,name='action'),
	path('pendingrequest',views.pending,name='pending'),
    path('edited_event_requests',views.editedeventrequests,name='editedeventrequests'),
    path('<int:eventid>/showchanges',views.showchanges,name='showchanges'),
    path('<int:eventid>/<str:action>/changeevent',views.changeevent,name='changeevent')
]
