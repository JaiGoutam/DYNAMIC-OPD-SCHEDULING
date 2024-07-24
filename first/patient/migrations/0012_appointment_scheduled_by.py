# Generated by Django 5.0.3 on 2024-05-10 11:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0011_remove_appointment_time_delete_slot'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='scheduled_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='patient.doctor'),
        ),
    ]
