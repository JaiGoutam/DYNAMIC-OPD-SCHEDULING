# forms.py

from django import forms
from patient.models import Doctor
from django.utils import timezone

class DoctorSelectionForm(forms.Form):
    doctor = forms.ModelChoiceField(queryset=Doctor.objects.all(), empty_label=None)
    date = forms.DateField(initial=timezone.now().date())



