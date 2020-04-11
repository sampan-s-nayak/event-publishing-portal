from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# Create your models here.

class Event(models.Model):
    owner = models.ForeignKey(User,on_delete=models.CASCADE,related_name='events_created+')
    event_name = models.CharField(max_length=40)
    event_description = models.CharField(max_length=400)
    event_start_date = models.DateField()
    event_end_date = models.DateField()
    verified = models.BooleanField(default=False)
    ended = models.BooleanField(default=False)
    max_participants = models.PositiveIntegerField(null=True)
    num_participants = models.PositiveIntegerField(default=0)
    max_waiting_list_size = models.PositiveIntegerField(null=True)
    num_in_waiting_list = models.PositiveIntegerField(default=0)
    assigned_mod = models.ForeignKey(User,on_delete=models.CASCADE,related_name='assigned_admin+',default=1)
    
    def __str__(self):
        return self.event_name
    
class Registration(models.Model):
    participant = models.ForeignKey(User,on_delete=models.CASCADE,related_name='events_registered+')
    event = models.ForeignKey(Event,on_delete=models.CASCADE,related_name='participants+')

class WaitingList(models.Model):
    participant = models.ForeignKey(User,on_delete=models.CASCADE,related_name='events_waiting+')
    event = models.ForeignKey(Event,on_delete=models.CASCADE,related_name='waiting_list+')
    added_time = models.DateTimeField()

class EditEvent(models.Model):
    event = models.ForeignKey(Event,on_delete=models.CASCADE,related_name='event+')
    newname = models.CharField(max_length=40)
    newdescription = models.CharField(max_length=400)
    newstart_date = models.DateField()
    newend_date = models.DateField()
    newmax_participants = models.PositiveIntegerField()
    newmax_waiting_list_size = models.PositiveIntegerField()
