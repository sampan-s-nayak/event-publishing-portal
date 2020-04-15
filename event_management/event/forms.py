from django import forms
from .models import EditEvent,Event
from django.core.exceptions import ValidationError
from datetime import date


class EditEventForm(forms.ModelForm):
    class Meta:
        model = EditEvent
        fields= ('newname','newdescription','newstart_date','newend_date','newmax_participants','newmax_waiting_list_size')
        labels={
            "newname":"New name",
            "newdescription":"New Description",
            "newstart_date":" New start date",
            "newend_date":"New end date",
            "newmax_participants":"New maximum participants",
            "newmax_waiting_list_size":"New maximum waiting list size"
        }
        widgets = {
            'newstart_date': forms.DateInput(format=('%d/%m/%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
            'newend_date': forms.DateInput(format=('%d/%m/%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
        }
    
    def checkreg(self):
        if self.cleaned_data["newmax_participants"]<Event.objects.get(pk = self.event.id).num_participants:
            raise  ValidationError(str(Event.objects.get(pk = self.event.id).num_participants) + " have already registered")
        return self.cleaned_data["newmax_participants"]

    def checkwait(self):
        if self.cleaned_data["newmax_waiting_list_size"]<Event.objects.get(pk = self.event.id).num_in_waiting_list:
            raise  ValidationError(str(Event.objects.get(pk = self.event.id).num_in_waiting_list) + " have already registered")
        return self.cleaned_data["newmax_waiting_list_size"] 

    def checkstart(self):
        if self.cleaned_data["newstart_date"]>self.cleaned_data["newend_date"]:
            raise ValidationError("Start date cannot be before end date")
        elif self.cleaned_data["newstart_date"]<date.today():
            raise ValidationError("Please select a date from today")
        return self.cleaned_data["newstart_date"]
            
