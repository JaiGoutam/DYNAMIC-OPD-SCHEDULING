from django.contrib import admin
from patient.models import patient
from patient.models import Doctor
from patient.models import Appointment

# Register your models here.
class patientAdmin(admin.ModelAdmin):
    list_display=('name','email','address','height','weight','dob','gender','password')

admin.site.register(patient,patientAdmin)


class DoctorAdmin(admin.ModelAdmin):
    list_display=('name', 'speciality', 'current_load')

admin.site.register(Doctor,DoctorAdmin)


class AppointmentAdmin(admin.ModelAdmin):
    list_display=('patient','date','is_completed','appointment_file', 'queue_position', 'urgency', 'scheduled_by', 'arrival_time', 'service_start_time', 'service_end_time', 'location_wait_time', 'estimated_start_service_time')

admin.site.register(Appointment,AppointmentAdmin)


