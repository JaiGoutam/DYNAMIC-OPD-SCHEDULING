from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render,redirect,get_object_or_404
from patient.models import patient
from django.core.mail import send_mail
from django.conf import settings
import random
from datetime import datetime, timedelta, time

from django.contrib import messages
from patient.models import Doctor,Appointment,patient
from django.http import JsonResponse
from django.http import HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
import os


from datetime import datetime, timedelta
from django.utils import timezone
from django.utils.timezone import now







def patientregistration(request):#register details after email verification
    if request.method=="POST":
        name=request.POST.get('name')
        address=request.POST.get('address')
        height=request.POST.get('height')
        weight=request.POST.get('weight')
        dob=request.POST.get('dob')
        gender=request.POST.get('gender')
        email = request.session.get('email')
        password = request.session.get('password')
        en=patient(name=name,email=email,address=address,height=height,weight=weight,dob=dob,gender=gender,password=password)
        en.save()
        del request.session['email']
        del request.session['password']
        return redirect('login')

    return render(request,"patientregistration.html")



def register(request):#email register page which accept email and password
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        verify_password = request.POST.get('verify_password')

        if check_email_exists(email):
            messages.warning(request, 'Email already Registered with an account')
            return redirect('register')
        
        else:
            
        
            if password == verify_password:
                generated_otp = generate_otp()
                send_otp_email(email, generated_otp)
                request.session['generated_otp'] = generated_otp
                request.session['email'] = email
                request.session['password'] = password

                return redirect('verify_otp')
            else:
                messages.warning(request, 'Passwords did not match')
                return redirect('register')
    
    return render(request, 'register.html')

def verify_otp(request):# verify otp page 
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        generated_otp = request.session.get('generated_otp')
        
        if generated_otp == entered_otp:
            messages.success(request, 'Successfully Registered')
            # Proceed with user registration
            
            # Clear session data

            del request.session['generated_otp']
            return redirect('patientregistration') # Redirect to the home page after registration

        else:
            messages.warning(request, 'Invalid OTP. Please try again.')
            return redirect('verify_otp')
    
    return render(request, 'verify_otp.html')

def generate_otp():#function to generate otp
    return ''.join([str(random.randint(0, 9)) for _ in range(6)])

def send_otp_email(email, otp):#function to send otp in mail 
    subject = 'OTP Verification'
    message = otp
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list,fail_silently=False)

def check_email_exists(email): #checks that email exist or not in model
    user = patient.objects.filter(email=email).first()
    if user:
        return True
    else:
        return False
    

def login_register(request): #starting page of app to show login and register buttons
    return render(request, 'login_register.html')

def login(request): #login page with gmail and password
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        pt = patient.objects.filter(email=email).first()
        if pt is not None:
            if pt.password == password:
                request.session['patient_id'] = pt.id
                return redirect('home') # return redirect('user_home', patient_id=patient.id)
            else:
                messages.warning(request, 'Wrong password')
                return redirect('login')
        else:
            messages.warning(request, 'Email is not registered')
            return redirect('login')
    else:
        return render(request, 'login.html')

def home(request):#starting home page after login
    patient_id = request.session.get('patient_id')
    if patient_id is not None:
        # Render home.html with patient_id
        pt = patient.objects.get(id=patient_id)
        return render(request, 'home.html', {'pt': pt})
    else:
        # Redirect to login if patient_id is not present in session
        return redirect('login')

def scheduled_appointment(request):
    patient_id = request.session.get('patient_id')
    
    if patient_id is not None:
        existing_appointment = Appointment.objects.filter(patient_id=patient_id, is_completed=False,date__gte=now().date()).first()
        if existing_appointment:
            return redirect('appointment_in_process')
        else:
            patient_obj = patient.objects.get(id=patient_id)
            context = {'patient': patient_obj}
            return render(request, 'scheduled_appointment.html', context)
    else:
        return redirect('login')

#bvkjbdozkbobfdobvof'bvofbvorobbvdf
#changes start
def appointment_in_process(request):
    patient_id = request.session.get('patient_id')
    if patient_id:
        try:
            appointment = Appointment.objects.filter(patient_id=patient_id, is_completed=False,date__gte=now().date()).first()
            
            
            return render(request, 'appointment_in_process.html', {'appointment': appointment })
        except Appointment.DoesNotExist:
            pass
    return render(request, 'appointment_in_process.html')

def delete_appointment(request):
    appointment_id = request.POST.get('appointment_id')
    if appointment_id:
        try:
            appointment = Appointment.objects.get(id=appointment_id)
            subsequent_appointments = Appointment.objects.filter(queue_position__gt=appointment.queue_position, is_completed=False)
            for subsequent_appointment in subsequent_appointments:
                subsequent_appointment.queue_position -= 1
                subsequent_appointment.save()
            appointment.delete()
            update_estimated_start_service_time_for_appointments_of_today()
            return redirect('home')
        except Appointment.DoesNotExist:
            pass
    return redirect('appointment_in_process')


def calculate_queue_position(urgency, location_wait_time):
    now = timezone.now()

    all_appointments = Appointment.objects.order_by('queue_position')
    appointments = Appointment.objects.filter(is_completed=False, date=now.date()).order_by('queue_position')

    if appointments.count() == 0:
        max_queue_position = all_appointments.last().queue_position if all_appointments.exists() else 0
        return max_queue_position + 1

    new_queue_position = None

    for appointment in appointments:
        time_elapsed = (now - appointment.arrival_time).total_seconds() / 60
        remaining_wait_time = max(appointment.location_wait_time - time_elapsed, 0)
        
        if (location_wait_time < remaining_wait_time) or (
            location_wait_time == remaining_wait_time and urgency > appointment.urgency):
            new_queue_position = appointment.queue_position
            break

    if new_queue_position is None:
        new_queue_position = appointments.last().queue_position + 1
    else:
        for appointment in appointments:
            if appointment.queue_position >= new_queue_position:
                appointment.queue_position += 1
                appointment.save()

    return new_queue_position


#CHANGE FOR LOCATION 
#START
LOCATION_WAIT_TIMES = {
    'A': 10,
    'B': 20,
    'C': 30,
    'D': 40,
    'E': 50,
}
def book_appointment(request):
    if request.method == 'POST':
        # Fetching patient details from session
        patient_id = request.session.get('patient_id')
        if not patient_id:
            return redirect('login')

        # Fetching patient object
        patient_obj = patient.objects.get(id=patient_id)

        date = request.POST.get('date')
        location = request.POST.get('location')
        temperature = request.POST.get('temperature')
        heart_rate = request.POST.get('heart_rate')
        primary_complaints = request.POST.get('primary_complaints')
        cough = request.POST.get('cough')
        body_pain = request.POST.get('body_pain')
        headache = request.POST.get('headache')
        follow_up = request.POST.get('follow_up')
        is_pregnant = request.POST.get('is_pregnant')
        age = patient_obj.calculate_age()

        

        urgency = 0
        if(follow_up):
            urgency += 2
        if patient_obj.gender == 'female' :
            urgency += 1
            if(is_pregnant):
                urgency += 2
        if((14 >= age and age >= 10) or (age >= 60 and age <= 75)):
            urgency += 1
        if(age < 10 or age > 75 ):
            urgency += 2
        if cough:
            urgency += 1
        if body_pain:
            urgency += 1
        if temperature:
            temperature = float(temperature)
            if 98 > temperature or temperature > 101:
                urgency += 1
        if headache:
            urgency += 1


        selected_date = datetime.strptime(date, '%Y-%m-%d').date()
        
        if selected_date < datetime.now().date():
            messages.error(request, 'Invalid date selected.')
            return redirect('appointment_form')

        # Calculating queue position based on urgency
        location_wait_time = LOCATION_WAIT_TIMES.get(location)
        queue_position = calculate_queue_position(urgency, location_wait_time)

        # Creating appointment object
        
        appointment = Appointment.objects.create(
            patient=patient_obj,
            queue_position=queue_position,
            date=date,
            is_completed=False,
            urgency=urgency,
            arrival_time = timezone.now(),
            location_wait_time = location_wait_time
        )
        
        
        # Constructing appointment file content
        file_content = f"Patient Name: {patient_obj.name}\nGender: {patient_obj.gender}\nAge: {age}\nIs Pregnant: {is_pregnant}\nFollow-up: {follow_up}\n"
        file_content += f"Temperature: {temperature}\nHeart Rate: {heart_rate}\nPrimary Complaints: {primary_complaints}\nCough: {cough}\nBody Pain: {body_pain}\nHeadache: {headache}"

        if follow_up:
            last_appointment = Appointment.objects.filter(patient=patient_obj, is_completed=True).order_by('-date').first()
            if last_appointment and last_appointment.scheduled_by:
                file_content += (
                    f"\nLast Doctor: {last_appointment.scheduled_by.name}\n"
                    f"Last Appointment Date: {last_appointment.date.strftime('%Y-%m-%d')}"
                )

        # Saving the appointment file
        appointment_file_path = os.path.join('appointments', f'appointment_{appointment.id}.txt')
        appointment.appointment_file.save(appointment_file_path, ContentFile(file_content))


        # Saving the appointment file
        appointment_file_path = os.path.join('appointments', f'appointment_{appointment.id}.txt')
        appointment.appointment_file.save(appointment_file_path, ContentFile(file_content))
        

        messages.success(request, 'Appointment booked successfully! Your queue position is {}'.format(queue_position))
        update_estimated_start_service_time_for_appointments_of_today()
        return redirect('success')
    else:
        return HttpResponse('Invalid request method')


def success(request):
    return render(request, 'success.html')



def user(request):#user dashboard page on the bottom right corner
    patient_id = request.session.get('patient_id')
    if patient_id is not None:
        pt = patient.objects.get(id=patient_id)
        # Render user.html with patient_id
        return render(request, 'user.html', {'pt': pt})
    else:
        # Redirect to login if patient_id is not present in session
        return redirect('login')
    

def edit_profile(request):#user/edit profile (to edit patient details)
    patient_id = request.session.get('patient_id')
    if patient_id is not None:
        pt = patient.objects.get(id=patient_id)
        if request.method == 'POST':
            pt.name = request.POST['name']
            pt.height = request.POST['height']
            pt.weight = request.POST['weight']
            pt.dob = request.POST['dob']
            pt.save()
            return redirect('user')
        else:
            return render(request, 'edit_profile.html', {'pt': pt})
    else:
        # Redirect to login if patient_id is not present in session
        return redirect('login')
    

def privacy_policy(request):#user/privacy_policy   application privacy and policy
    return render(request, 'privacy_policy.html')

def help(request):#user/help   application help page
    return render(request, 'help.html')

def about_us(request):#user/about_us   application about us page
    return render(request, 'about_us.html')

def delete_account(request):#user/delete account   logic to delete account
    patient_id = request.session.get('patient_id')
    if patient_id is not None:
        pt = patient.objects.get(id=patient_id)
        if request.method == 'POST':
            pt.delete()
            del request.session['patient_id']
            return redirect('login')
        else:
            return render(request, 'delete_account.html', {'patient': patient})
    else:
        # Redirect to login if patient_id is not present in session
        return redirect('login')

def password_manager(request):#user/password_manager   password manager page

    patient_id = request.session.get('patient_id')
    if patient_id is not None:
        pt = patient.objects.get(id=patient_id)
        if request.method == 'POST':
            current_password = request.POST['current_password']
            new_password = request.POST['new_password']
            verify_new_password = request.POST['verify_new_password']
            if pt.password == current_password:

                if new_password == verify_new_password:
                    pt.password = new_password
                    pt.save()
                    messages.success(request, 'Password changed successfully.')
                    return redirect('user')
            
                else:
                    messages.error(request,'passwords are not same ')
                    return redirect('password_manager')
                            
            else:
                messages.error(request, 'Current password is not correct.')
                return redirect('password_manager')
        else:
            return render(request, 'password_manager.html', {'pt': pt})
    else:
        # Redirect to login if patient_id is not present in session
        return redirect('login')










############## DOCTOR FUNCTIONS ###############################





def doctor_schedule(request):
    if request.method == 'POST':
        doctor_id = request.POST.get('doctor')
        date = request.POST.get('date')

        # Validate date
        selected_date = datetime.strptime(date, '%Y-%m-%d').date()
        today = datetime.now().date()
        if selected_date < today or selected_date.weekday() == 6:  # If selected date is before today or Sunday
            return HttpResponseBadRequest("Invalid date selected.")

        return redirect('doctor_page', doctor_id=doctor_id)
    else:
        doctors = Doctor.objects.all()
        today = datetime.now().date()
        min_date = today
        if today.weekday() == 6:
            min_date += timedelta(days=1)
        return render(request, 'doctor_schedule.html', {'doctors': doctors, 'today': today, 'min_date': min_date})

from django.template.context_processors import csrf
@csrf_exempt
def doctor_page(request, doctor_id):
    doctor = Doctor.objects.get(id=doctor_id)
    today = now().date()
    appointments = Appointment.objects.filter(scheduled_by=doctor, is_completed=False, date=today).order_by('queue_position')
    context = {
        'doctor': doctor,
        'appointments': appointments,
        'csrf_token': csrf(request)['csrf_token']
    }
    return render(request, 'doctor_page.html', context)

def view_appointment_file(request, appointment_id):
    try:
        appointment = Appointment.objects.get(id=appointment_id)
        file_content = appointment.appointment_file.read()
        return HttpResponse(file_content, content_type='application/json')
    except Appointment.DoesNotExist:
        return HttpResponse("Appointment not found", status=404)
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", status=500)


from django.core.exceptions import ObjectDoesNotExist
@csrf_exempt
def start_appointment(request):
    if request.method == 'POST':
        appointment_id = request.POST.get('appointment_id')
    
        try:
            appointment = Appointment.objects.get(id=appointment_id)

            
            # Update the appointment's service_start_time and doctor's current_appointment
            appointment.service_start_time = timezone.now()
            appointment.save()
           
            return JsonResponse({'status': 'success'})
        except ObjectDoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Appointment or Doctor not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)


@csrf_exempt
def mark_completed(request):
    if request.method == 'POST':
        appointment_id = request.POST.get('appointment_id')
        doctor_id = request.POST.get('doctor_id')
        try:
            appointment = Appointment.objects.get(id=appointment_id)
            doctor = Doctor.objects.get(id=doctor_id)
           
            # Update the appointment's service_end_time and doctor's current_appointment
            appointment.service_end_time = timezone.now()
            appointment.is_completed = True
            #appointment.scheduled_by = doctor
            appointment.save()
            
            

            update_estimated_start_service_time_for_appointments_of_today()
            

            return JsonResponse({'status': 'success'})
        except ObjectDoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Appointment or Doctor not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)
    



@csrf_exempt
def appointments_data(request, doctor_id):
    appointments = Appointment.objects.filter(is_completed=False).order_by('queue_position')
    appointments_data = [{'patient_name': appointment.patient.name, 'date': appointment.date.strftime('%Y-%m-%d'), 'time': appointment.time.strftime('%H:%M'), 'is_completed': appointment.is_completed} for appointment in appointments]
    return JsonResponse(appointments_data, safe=False)








#---------------------------------- Doctor Performance Analyze ---------------------------------------#


from django.db.models import Count, Avg, F, ExpressionWrapper, DurationField
import json

def doctor_performance(request):
    today = timezone.now().date()
    one_week_ago = today - timedelta(days=7)
    one_month_ago = today - timedelta(days=30)

    # Get weekly and monthly appointment counts for each doctor
    weekly_appointments = Appointment.objects.filter(
        date__gte=one_week_ago,
        date__lte=today,
        is_completed=True
    ).values('scheduled_by__name').annotate(appointment_count=Count('id'))

    monthly_appointments = Appointment.objects.filter(
        date__gte=one_month_ago,
        date__lte=today,
        is_completed=True
    ).values('scheduled_by__name').annotate(appointment_count=Count('id'))

    # Get average service times for each doctor
    weekly_avg_service_time = Appointment.objects.filter(
        date__gte=one_week_ago,
        date__lte=today,
        is_completed=True
    ).values('scheduled_by__name').annotate(
        avg_service_time=Avg(ExpressionWrapper(F('service_end_time') - F('service_start_time'), output_field=DurationField()))
    )

    monthly_avg_service_time = Appointment.objects.filter(
        date__gte=one_month_ago,
        date__lte=today,
        is_completed=True
    ).values('scheduled_by__name').annotate(
        avg_service_time=Avg(ExpressionWrapper(F('service_end_time') - F('service_start_time'), output_field=DurationField()))
    )

    weekly_avg_service_time = list(weekly_avg_service_time)
    for entry in weekly_avg_service_time:
        entry['avg_service_time'] = entry['avg_service_time'].total_seconds() * 1000  # Convert to milliseconds

    monthly_avg_service_time = list(monthly_avg_service_time)
    for entry in monthly_avg_service_time:
        entry['avg_service_time'] = entry['avg_service_time'].total_seconds() * 1000  # Convert to milliseconds


    context = {
        'weekly_appointments_json': json.dumps(list(weekly_appointments)),
        'monthly_appointments_json': json.dumps(list(monthly_appointments)),
        'weekly_avg_service_time_json': json.dumps(list(weekly_avg_service_time), default=str),
        'monthly_avg_service_time_json': json.dumps(list(monthly_avg_service_time), default=str),
    }

    return render(request, 'doctor_performance.html', context)



#---------------------------------- Queuing Logics ----------------------------------------------------#

from django.db.models import Avg, F, ExpressionWrapper, DurationField

def service_time(doctor):
    completed_appointments = Appointment.objects.filter(scheduled_by=doctor, is_completed=True)
    if not completed_appointments.exists():
        return None

    total_service_time = completed_appointments.aggregate(
        average_duration=Avg(ExpressionWrapper(F('service_end_time') - F('service_start_time'), output_field=DurationField()))
    )['average_duration']

    return total_service_time

def average_service_time_all_doctors():
    doctors = Doctor.objects.all()
    service_times = []
    for doctor in doctors:
        service_time_value = service_time(doctor)
        if service_time_value is not None:
            service_times.append(service_time_value)

    if not service_times:
        return None

    # Calculate the average service time across all doctors
    average_service_time = sum(service_times, timedelta()) / len(service_times)
    return average_service_time


def estimated_start_service_time(appointment):
    if appointment.is_completed:
        return appointment.service_start_time

    # Get the average service time across all doctors
    avg_service_time = average_service_time_all_doctors()
    #if not avg_service_time:
    #    return None  # No completed appointments to estimate service time

    # Get the current time
    current_time = timezone.now()
    
    # Find the number of appointments before the current one in the queue
    earlier_appointments = Appointment.objects.filter(
        date=appointment.date,
        queue_position__lt=appointment.queue_position,
        is_completed=False
    ).count()

   # Calculate the estimated wait time and start service time
    estimated_wait_time = earlier_appointments * avg_service_time
    estimated_start_time = current_time + estimated_wait_time

    # Calculate the time elapsed since the patient's arrival and the remaining wait time
    time_elapsed = (current_time - appointment.arrival_time).total_seconds() / 60
    remaining_wait_time = max(appointment.location_wait_time - time_elapsed, 0)

    # Determine the later of the two times
    final_estimated_time = max(estimated_start_time, current_time + timedelta(minutes=remaining_wait_time))

    return final_estimated_time

def update_estimated_start_service_time_for_appointments_of_today():
    appointments = Appointment.objects.filter(date=timezone.now().date(), is_completed=False)
    for appointment in appointments:
        appointment.estimated_start_service_time = estimated_start_service_time(appointment)
        appointment.save()






# start
#recepnist



# views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.utils import timezone


def receptionist_dashboard(request):
    # Filter appointments that are not completed and do not have a scheduled doctor
    appointments = Appointment.objects.filter(
        is_completed=False, date__gte=timezone.now().date(), scheduled_by__isnull=True
    ).order_by('queue_position')
    
    

    
    doctors = Doctor.objects.all()
    
    return render(request, 'receptionist_dashboard.html', {'appointments': appointments, 'doctors': doctors})

def show_appointment_file(request, appointment_id):
    try:
        appointment = Appointment.objects.get(id=appointment_id)
        return HttpResponse(appointment.appointment_file.read(), content_type='application/json')
    except Appointment.DoesNotExist:
        return HttpResponse("Appointment not found", status=404)
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", status=500)
    
from django.utils.dateparse import parse_date

def all_appointments(request):
    # Get all appointments ordered by queue position
    all_appointments = Appointment.objects.all().order_by('-queue_position')
    
    selected_date = request.GET.get('date')
    if selected_date:
        selected_date = parse_date(selected_date)
        all_appointments = all_appointments.filter(date=selected_date)
    
    return render(request, 'all_appointments.html', {'all_appointments': all_appointments, 'selected_date': selected_date})

def add_remarks(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    doctors = Doctor.objects.all()
    if request.method == 'POST':
        remarks = request.POST.get('remarks')
        # Append the remarks to the appointment file
        if appointment.appointment_file:
            with open(appointment.appointment_file.path, 'a') as f:
                f.write(f"\nRemarks: {remarks}")
        appointment.save()
        return HttpResponse(status=200)  # Return a success status, can be customized as per your needs
    return render(request, 'receptionist_dashboard.html', {'appointments': appointment, 'doctors': doctors})

def assign_doctor(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    doctors = Doctor.objects.all()
    if request.method == 'POST':
        appointment.scheduled_by = Doctor.objects.get(id=request.POST.get('scheduled_by'))
        
        appointment.save()
        
        return HttpResponse(status=200)    
      # Return a success status, can be customized as per your needs
    return render(request, 'receptionist_dashboard.html', {'appointments': appointment, 'doctors': doctors})
