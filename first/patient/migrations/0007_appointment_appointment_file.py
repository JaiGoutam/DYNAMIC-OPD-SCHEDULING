# Generated by Django 5.0.3 on 2024-05-03 05:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0006_remove_doctor_schedule_doctor_speciality'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='appointment_file',
            field=models.FileField(blank=True, null=True, upload_to='appointments/'),
        ),
    ]
