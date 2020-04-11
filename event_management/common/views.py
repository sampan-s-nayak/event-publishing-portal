from django.shortcuts import render
from .models import *
from .forms import SearchForm
from event import models as eventmod
# Create your views here.


def search(request):
	if request.method == 'GET':
		print("method rec success")
		form = SearchForm(request.GET)
		if form.is_valid():
			eventreq = form.cleaned_data["search"]
			allevents= eventmod.Event.objects.all().filter( event_name__contains=eventreq)
			return render(request,'common/home.html',{'eventlist':allevents,"form":form})
		else:
			form = SearchForm()
			allevents= eventmod.Event.objects.all()		
			return render(request,"common/home.html",{'eventlist':allevents,"form":form})
	else:		
		form = SearchForm()
		allevents= eventmod.Event.objects.all()		
		return render(request,"common/home.html",{'eventlist':allevents,"form":form})	

	
