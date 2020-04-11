from django.db import models
from django.contrib.auth.models import User
from event.models import Event

class ReportedUsers(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,related_name='reported')
    reported_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True,related_name='reported_users')
    reason = models.CharField(max_length=400)