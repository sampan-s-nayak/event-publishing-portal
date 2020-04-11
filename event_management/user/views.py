from django.shortcuts import render, redirect
from .models import ReportedUsers
from event import models as eventmod
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import Report_user_form
from django.contrib.auth.models import User, Group

# Create your views here.
@login_required
def create_event(request):
    return render(request,'users/create_event.html')

@login_required
def add_event(request):
    current_user = request.user
    Event_name = request.POST['Name']
    Event_desc = request.POST['Desc']
    Start_date = request.POST['Start_Date']
    End_date = request.POST['End_Date']
    Max_part = request.POST['Max']
    Num_part = request.POST['Num']
    Max_list = request.POST['Max_List']
    Num_list = request.POST['Num_List']
    event = eventmod.Event(owner=current_user,event_name=Event_name,event_description=Event_desc, event_start_date=Start_date,event_end_date=End_date, max_participants=Max_part,num_participants=Num_part, max_waiting_list_size=Max_list,num_in_waiting_list=Num_list)
    event.save()
    return render(request,'users/create_event.html')    

@login_required
def display_events(request):
    all_events = eventmod.Event.objects.all()
    return render(request,'users/display_events.html',{'key': all_events})

@login_required      
def hosted_events(request):
    current_user = request.user
    all_events = eventmod.Event.objects.filter(owner=current_user)
    return render(request,'users/hosted_events.html',{'key': all_events})

@login_required
def report_user(request,id):
    template_path = 'users/report_user.html'
    user = User.objects.get(id=id)

    if(request.method == 'POST'):
        f = Report_user_form(request.POST)

        if f.is_valid():
            report = f.save()
            report.user = user
            report.reported_by = request.user
            report.save()
        return redirect(request.META['HTTP_REFERER']) #  fix this later

    form = Report_user_form()
    context = {
        'form':form,
        'user':user
    }

    return render(request,template_path,context)

@login_required
def createdevents(request):
    return render(request,"users/eventlist.html",{'createdevents':eventmod.Event.objects.filter(owner=request.user)})

@login_required
def joinedevents(request):
    return render(request,"users/eventlist.html",{'joinedevents':eventmod.Registration.objects.filter(participant=request.user)})

@login_required
def getregistrations(request,eventid):
    return render(request,"users/registrationlist.html",{'registrationlist':eventmod.Registration.objects.filter(event_id=eventid)})

@login_required
def dashboard(request):
    #Group.objects.get(name='Moderator').user_set.add(User.objects.get(username='sspa'))
    return render(request,"users/dashboard.html",{'user':request.user,'is_mod':request.user.groups.filter(name='Moderator').exists()})
    
    
    
    
