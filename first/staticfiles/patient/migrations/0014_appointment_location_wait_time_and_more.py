# Generated by Django 5.0.3 on 2024-06-05 04:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0013_appointment_arrival_time_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='location_wait_time',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='urgency',
            field=models.IntegerField(),
        ),
    ]
