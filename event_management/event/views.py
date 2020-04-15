from django.shortcuts import render,redirect
from datetime import datetime,date
from .models import *
from django.db.models import F
from .forms import EditEventForm
from django.contrib.auth.decorators import login_required
from moderator import models as modmod


# Create your views here.

def eventdetails(request,eventid):
	eventobj = Event.objects.all().get(pk = eventid)
	participantsobj = Registration.objects.all().filter(event_id = eventid)
	waitinglistsize = WaitingList.objects.filter(event_id = eventid).count()
	userreg = None
	if request.user.is_authenticated:
		userreg = Registration.objects.filter(participant=request.user,event = eventobj).exists() or WaitingList.objects.filter(participant=request.user,event = eventobj).exists()
	return render(request,"event/eventdetails.html",{'eventobj':eventobj,'participantsobj':participantsobj,'userreg':userreg,'waitinglistsize':waitinglistsize})

@login_required
def eventregister(request,regeventid):
	eventobj = Event.objects.all().filter(pk = regeventid)
	if modmod.BlackList.objects.filter(user=request.user).exists():
		blacklistobj = modmod.BlackList.objects.get(user=request.user)
		if date.today()-blacklistobj.added_time>blacklistobj.duration:
			blacklistobj.delete()
		else:
			return render(request,"event/oops.html",{'reason':'You have been blacklisted for another ' + str(blacklistobj.duration-date.today()-blacklistobj.added_time) + 'days'})
	if Registration.objects.filter(participant = request.user).exists():
		return render(request,"event/oops.html",{'reason':'You have already registered for the event'})
	


	else:
		if eventobj.first().num_participants==eventobj.first().max_participants:
			WaitingList(participant = request.user,event_id = regeventid,added_time=datetime.now()).save()
		else:
			Registration(event = eventobj.first(),participant = request.user).save()
			eventobj.update(num_participants = F('num_participants')+1)
	return redirect("/event/"+str(regeventid))

@login_required
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
		if eventobj.event_end_date<date.today():
			return render(request,"event/oops.html",{'reason':'The event no longer exists'})
	except Event.DoesNotExist:
		return render(request,"event/oops.html",{'reason':'The event no longer exists'})
	if EditEvent.objects.filter(event=eventobj).exists():
		return render(request,"event/oops.html",{'reason':'An modification request has already been sent'})
	if request.method=="POST":
		form = EditEventForm(request.POST)
		if form.is_valid():
			if form.cleaned_data["newstart_date"]>form.cleaned_data["newend_date"]:
				return render(request,"event/oops.html",{'reason':'Start date cannot be before end date'})
			if form.cleaned_data["newmax_participants"]<eventobj.num_participants:
				return render(request,"event/oops.html",{'reason':str(eventobj.num_participants) + ' have already registered'})
			if form.cleaned_data["newmax_waiting_list_size"]<eventobj.num_in_waiting_list:
				return render(request,"event/oops.html",{'reason':str(eventobj.num_in_waiting_list) + ' are already in the waiting list'})
		
			EditEvent(event = eventobj,newname=form.cleaned_data["newname"],newdescription=form.cleaned_data["newdescription"],newstart_date=form.cleaned_data["newstart_date"],newend_date=form.cleaned_data["newend_date"],newmax_participants=form.cleaned_data["newmax_participants"],newmax_waiting_list_size=form.cleaned_data["newmax_waiting_list_size"]).save()
			return redirect("/event/"+str(eventid))
		else:
			return render(request,"event/oops.html",{'reason':'Some error occurred!Please try again later'})
	else:
		return render(request,"event/editevent.html",{'form':EditEventForm(initial={'newname':eventobj.event_name,'newdescription':eventobj.event_description,'newstart_date':eventobj.event_start_date,'newend_date':eventobj.event_end_date,'newmax_participants':eventobj.max_participants,'newmax_waiting_list_size':eventobj.max_waiting_list_size})})

