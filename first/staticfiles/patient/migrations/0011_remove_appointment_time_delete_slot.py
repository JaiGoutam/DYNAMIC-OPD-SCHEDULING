# Generated by Django 5.0.3 on 2024-05-10 05:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0010_remove_appointment_doctor'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='time',
        ),
        migrations.DeleteModel(
            name='Slot',
        ),
    ]
