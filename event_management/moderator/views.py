from django.shortcuts import render,redirect
from .models import BlackList
from user.models import ReportedUsers
from django.contrib.auth.models import User
from event.models import EditEvent,Event

BLACKLIST_DURATION = 7

# Create your views here.
def blacklist(request,id,duration):
    # TODO authentication to be added

    user = User.objects.get(id=id)
    if(not BlackList.objects.filter(user=user).exists()):
        bl = BlackList.objects.create(user=user,duration=duration)
    return redirect('view_reported_users')

def view_reported_users(request):
    # TODO authentication to be added

    template_path = 'moderator/reported_users.html'
    reported_users = ReportedUsers.objects.all()

    context = {
        'complaints': reported_users,
        'duration': BLACKLIST_DURATION,
    }
    return render(request, template_path,context)

def editedeventrequests(request):
    events = []
    for editevent in EditEvent.objects.all():
        if editevent.event.assigned_mod==request.user:
            events.append(editevent)
    return render(request,"moderator/edited_event_requests.html",{'events':events})

def showchanges(request,eventid):
    return render(request,"moderator/show_edited_event.html",{'event':EditEvent.objects.get(event_id = eventid)})

def pending(request):
	moderatorid=request.user.id;
	pendingobj=Event.objects.all().filter(assigned_mod_id=moderatorid,verified = 0 )
	return render(request,"moderator/pendingrequests.html",{'events':pendingobj})

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
