# Generated by Django 3.0.4 on 2020-04-07 11:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reportedusers',
            name='reported_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reported_users', to=settings.AUTH_USER_MODEL),
        ),
    ]
