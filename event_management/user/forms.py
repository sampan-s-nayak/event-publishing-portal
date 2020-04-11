from django.forms import ModelForm
from .models import ReportedUsers

class Report_user_form(ModelForm):
    class Meta:
        model = ReportedUsers
        fields = ['reason']
        