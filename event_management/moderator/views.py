from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import BlackList
from user.models import ReportedUsers
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from event.models import EditEvent,Event

BLACKLIST_DURATION = 7
    
@login_required
def blacklist_user(request,id,duration):
    user = request.user
    if(not user.is_staff or not user.is_superuser):
        return HttpResponse("you are not authorized to view this page") 

    user = User.objects.get(id=id)
    if(not BlackList.objects.filter(user=user).exists()):
        bl = BlackList.objects.create(user=user,duration=duration)
    return redirect('moderator:view_reported_users')

@login_required
def view_reported_users(request):
    user = request.user
    if(not user.is_staff or not user.is_superuser):
        return HttpResponse("you are not authorized to view this page") 

    template_path = 'moderator/reported_users.html'
    reported_users = ReportedUsers.objects.all()

    context = {
        'complaints': reported_users,
        'duration': BLACKLIST_DURATION,
    }
    return render(request, template_path,context)

@login_required
def editedeventrequests(request):
    events = []
    for editevent in EditEvent.objects.all():
        if editevent.event.assigned_mod==request.user:
            events.append(editevent)
    return render(request,"moderator/edited_event_requests.html",{'events':events})

@login_required
def showchanges(request,eventid):
    return render(request,"moderator/show_edited_event.html",{'event':EditEvent.objects.get(event_id = eventid)})

@login_required
def pending(request):
	moderatorid=request.user.id;
	pendingobj=Event.objects.all().filter(assigned_mod_id=moderatorid,verified = 0 )
	return render(request,"moderator/pendingrequests.html",{'events':pendingobj})

@login_required
def action(request,eventid,decision):
	if	decision=="accept":
		eventobj=Event.objects.all().get(pk=eventid)
		eventobj.verified=1;
		eventobj.save();
		return render(request,"moderator/decision.html",{'option':"accepted"})
	elif decision=="reject":
		eventobj=Event.objects.all().get(pk=eventid)
		eventobj.delete();
		return render(request,"moderator/decision.html",{'option':"rejected"})
	

@login_required
def changeevent(request,eventid,action):
    try:
        EditEvent.objects.get(event_id = eventid)
    except EditEvent.DoesNotExist:
        return render(request,"user/oops.html",{'reason':'The request has already been resolved'})
    if action=='reject':
        EditEvent.objects.get(event_id = eventid).delete()
        return redirect("/moderator/edited_event_requests")
    editeventobj = EditEvent.objects.get(event_id = eventid)
    eventobj = EditEvent.objects.get(event_id = eventid).event
    eventobj.event_name = editeventobj.newname
    eventobj.event_description = editeventobj.newdescription
    eventobj.event_start_date = editeventobj.newstart_date
    eventobj.event_end_date = editeventobj.newend_date
    eventobj.max_participants = editeventobj.newmax_participants
    eventobj.event_max_waiting_list_sizename = editeventobj.newmax_waiting_list_size
    eventobj.save()
    editeventobj.delete()
    return redirect("/moderator/edited_event_requests")
