from django.db import models
from django.contrib.auth.models import User

class UserData(models.Model):
    # TODO: add more attributes
    user = models.OneToOneField(User,related_name='data', on_delete=models.CASCADE,null=True)
    dob = models.DateField()
    ph_no = models.PositiveIntegerField()
    # user model stores email,so I didnt repeat it here

    class Meta:
        verbose_name_plural = "UsersData"
        db_table = 'UserData'


