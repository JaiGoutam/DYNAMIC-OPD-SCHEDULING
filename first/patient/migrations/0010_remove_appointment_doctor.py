# Generated by Django 5.0.3 on 2024-05-09 11:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0009_appointment_urgency'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='doctor',
        ),
    ]
