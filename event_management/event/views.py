from django.shortcuts import render,redirect
from datetime import datetime,date
from .models import *
from django.db.models import F
from .forms import EditEventForm
from django.contrib.auth.decorators import login_required


# Create your views here.

def eventdetails(request,eventid):
	eventobj = Event.objects.all().get(pk = eventid)
	participantsobj = Registration.objects.all().filter(event_id = eventid)
	userreg = Registration.objects.filter(participant=request.user,event = eventobj).exists() or WaitingList.objects.filter(participant=request.user,event = eventobj).exists()
	return render(request,"event/eventdetails.html",{'eventobj':eventobj,'participantsobj':participantsobj,'userreg':userreg})


def eventregister(request,regeventid):
	eventobj = Event.objects.all().filter(pk = regeventid)
	if Registration.objects.filter(participant = request.user).exists():
		return render(request,"event/oops.html",{'reason':'You have already registered for the event'})
	else:
		if eventobj.first().num_participants==eventobj.first().max_participants:
			WaitingList(participant = request.user,event_id = regeventid,added_time=datetime.now()).save()
		else:
			Registration(event = eventobj.first(),participant = request.user).save()
			eventobj.update(num_participants = F('num_participants')+1)
	return redirect("/event/"+str(regeventid))

def eventdropout(request,dropeventid):
	eventobj = Event.objects.all().get(pk = dropeventid)
	if Registration.objects.filter(participant=request.user,event = eventobj).exists():
		Registration.objects.all().get(participant=request.user,event = eventobj).delete()
		newreg = WaitingList.objects.all().filter(event = eventobj).order_by('added_time').first()
		if newreg:
			Registration(event_id = dropeventid,participant = newreg.participant).save()
			newreg.delete()
		else:
			Event.objects.all().filter(pk=dropeventid).update(num_participants = F('num_participants')-1)
	else:
		WaitingList.objects.all().get(participant=request.user,event = eventobj).delete()
	return redirect("/event/"+str(dropeventid))

@login_required
def changedetails(request,eventid):
	try:
		eventobj = Event.objects.get(pk = eventid)
		if eventobj.event_end_date>date.today():
			return render(request,"events/oops.html",{'reason':'The event no longer exists'})
	except Event.DoesNotExist:
		return render(request,"events/oops.html",{'reason':'The event no longer exists'})
	if request.method=="POST":
		form = EditEventForm(request.POST)
		if form.is_valid:
			form.save()
			return redirect("/event/"+str(eventid))
		else:
			return render(request,"events/oops.html",{'reason':'Some error occurred!Please try again later'})
	else:
		return render(request,"event/editevent.html",{'form':EditEventForm(initial={'newname':eventobj.event_name,'newdescription':eventobj.event_description,'newstart_date':eventobj.event_start_date,'newend_date':eventobj.event_end_date,'newmax_participants':eventobj.max_participants,'newmax_waiting_list_size':eventobj.max_waiting_list_size})})

