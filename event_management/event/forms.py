from django import forms
from .models import EditEvent

class EditEventForm(forms.ModelForm):
    class Meta:
        model = EditEvent
        fields = "__all__" 