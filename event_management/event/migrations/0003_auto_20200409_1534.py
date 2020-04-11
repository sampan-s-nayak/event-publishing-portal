# Generated by Django 3.0.4 on 2020-04-09 10:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0002_event_assigned_admin'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='assigned_admin',
            new_name='assigned_mod',
        ),
        migrations.CreateModel(
            name='EditEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('newname', models.CharField(max_length=40)),
                ('newdescription', models.CharField(max_length=400)),
                ('newstart_date', models.DateField()),
                ('newend_date', models.DateField()),
                ('newmax_participants', models.PositiveIntegerField()),
                ('newmax_waiting_list_size', models.PositiveIntegerField()),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event+', to='event.Event')),
            ],
        ),
    ]
