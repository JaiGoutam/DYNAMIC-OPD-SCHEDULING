# symptom_checker/urls.py

from django.urls import path
from .views import symptom_checker_api , symptom_checker_form

urlpatterns = [
    path('', symptom_checker_form, name='symptom_checker_form'),
    path('api/symptom_checker/', symptom_checker_api, name='symptom_checker_api'),

]
