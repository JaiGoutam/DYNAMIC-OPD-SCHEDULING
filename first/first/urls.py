"""
URL configuration for first project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from first import views
from django.urls import path, include



urlpatterns = [
    path('admin/', admin.site.urls),

   

    path('', views.login_register, name='login_register'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('patientregistration/',views.patientregistration,name='patientregistration'),
    path('verify_otp/', views.verify_otp, name='verify_otp'),




    path('home/', views.home, name='home'),
    path('scheduled_appointment/', views.scheduled_appointment, name='scheduled_appointment'),
    path('book_appointment/',views.book_appointment, name='book_appointment'),
    path('success/', views.success, name='success'),


    path('user/', views.user, name='user'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('privacy_policy/', views.privacy_policy, name='privacy_policy'),
    path('password_manager/', views.password_manager, name='password_manager'),
    path('help/', views.help, name='help'),
    path('about_us/', views.about_us, name='about_us'),
    path('delete_account/', views.delete_account, name='delete_account'),
    path('appointment_in_process/', views.appointment_in_process, name='appointment_in_process'),
    path('delete_appointment/', views.delete_appointment, name='delete_appointment'),
   
   


    path('doctor_schedule/', views.doctor_schedule, name='doctor_schedule'),
    path('doctor_page/<int:doctor_id>/', views.doctor_page, name='doctor_page'),
    path('start_appointment/', views.start_appointment, name='start_appointment'),
    path('mark_completed/', views.mark_completed, name='mark_completed'),
    path('appointments_data/<int:doctor_id>/', views.appointments_data, name='appointments_data'),
    path('view_appointment_file/<int:appointment_id>/', views.view_appointment_file, name='view_appointment_file'),



    path('doctor_performance/', views.doctor_performance, name='doctor_performance'),

    path('receptionist/', views.receptionist_dashboard, name='receptionist_dashboard'),
    path('all_appointments/', views.all_appointments, name='all_appointments'),
    path('appointment/<int:appointment_id>/show/', views.show_appointment_file, name='show_appointment_file'),
    path('appointment/<int:appointment_id>/add_remarks/', views.add_remarks, name='add_remarks'),
    path('appointment/<int:appointment_id>/assign_doctor/', views.assign_doctor, name='assign_doctor'),

    path('symptom_checker/', include('symptom_checker.urls')),
    
]
