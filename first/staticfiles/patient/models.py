from django.db import models
from datetime import date
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


# Create your models here
class patient(models.Model):
    options = [
        ('male', 'male'),
        ('female', 'female'),
        ('others', 'others'),
    ]
    name=models.CharField(max_length=50)
    email=models.EmailField()
    address=models.TextField()
    height=models.IntegerField()
    weight=models.IntegerField()
    dob=models.DateField()
    gender = models.CharField(max_length=20, choices=options, default='male')
    password = models.CharField(max_length=20, default='1234')
    def calculate_age(self):
        today = date.today()
        age = today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))
        return age


class Doctor(models.Model):
    name = models.CharField(max_length=100)
    speciality =models.CharField(max_length=50, default='Internal medicine')
    current_load = models.IntegerField(default=0)

    
    
    def __str__(self):
        return self.name
    


class Appointment(models.Model):
    patient = models.ForeignKey(patient, on_delete=models.CASCADE)
    queue_position = models.IntegerField(default=0)
    date = models.DateField()
    is_completed = models.BooleanField(default=False)
    appointment_file = models.FileField(upload_to='appointments/', blank=True, null=True)
    urgency = models.IntegerField()
    scheduled_by = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True, blank=True)
    arrival_time = models.DateTimeField(blank=True, null=True)
    service_start_time = models.DateTimeField(blank=True, null=True)
    service_end_time = models.DateTimeField(blank=True, null=True)
    location_wait_time = models.IntegerField()
    estimated_start_service_time = models.DateTimeField(null=True, blank=True)


    def __str__(self):
        return f"Appointment for {self.patient.name} on {self.date}"
    

def calculate_doctor_load(doctor):
    today = date.today()
    return Appointment.objects.filter(scheduled_by=doctor, date=today, is_completed=False).count()

@receiver(post_save, sender=Appointment)
def update_doctor_load_on_save(sender, instance, **kwargs):
    if instance.scheduled_by:
        doctor = instance.scheduled_by
        doctor.current_load = calculate_doctor_load(doctor)
        doctor.save()

@receiver(post_delete, sender=Appointment)
def update_doctor_load_on_delete(sender, instance, **kwargs):
    if instance.scheduled_by:
        doctor = instance.scheduled_by
        doctor.current_load = calculate_doctor_load(doctor)
        doctor.save()
    
