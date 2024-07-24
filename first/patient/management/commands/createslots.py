from django.core.management.base import BaseCommand
from datetime import datetime, timedelta, date
from patient.models import Doctor, Slot

class Command(BaseCommand):
    help = 'Fill slots in the database'

    def add_arguments(self, parser):
        parser.add_argument('date', type=str, help='Date in YYYY-MM-DD format')

    def handle(self, *args, **kwargs):
        date_str = kwargs['date']
        try:
            today_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            self.stdout.write(self.style.ERROR('Invalid date format. Please use YYYY-MM-DD.'))
            return
        
        current_date = today_date

        doctors = Doctor.objects.all()
        for doctor in doctors:
            start_time = '09:00:00'
            end_time = '17:00:00'
            interval = 30  # interval in minutes
            for i in range(2):
                start = datetime.combine(today_date, datetime.strptime(start_time, '%H:%M:%S').time())
                end = start + timedelta(minutes=interval)
                while end <= datetime.combine(today_date, datetime.strptime(end_time, '%H:%M:%S').time()):
                    Slot.objects.create(doctor=doctor, date=today_date, start_time=start.time(), end_time=end.time(), is_free=True)
                    start = end
                    end = start + timedelta(minutes=interval)
                today_date = today_date + timedelta(days=1)
            today_date = current_date
        self.stdout.write(self.style.SUCCESS('Slots filled successfully!'))
