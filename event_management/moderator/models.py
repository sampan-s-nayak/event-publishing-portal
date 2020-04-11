from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class BlackList(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='blacklist')
    added_time = models.DateTimeField(auto_now_add=True, blank=True)
    duration = models.PositiveIntegerField()