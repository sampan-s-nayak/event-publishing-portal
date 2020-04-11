# Generated by Django 3.0.4 on 2020-04-01 12:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0003_auto_20200327_1333'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userdata',
            name='is_data_provided',
        ),
        migrations.AlterModelTable(
            name='event',
            table='Event',
        ),
        migrations.AlterModelTable(
            name='registration',
            table='Registration',
        ),
        migrations.AlterModelTable(
            name='userdata',
            table='UserData',
        ),
        migrations.AlterModelTable(
            name='waitinglist',
            table='WaitingList',
        ),
    ]