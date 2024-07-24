from django.core.management.base import BaseCommand
from datetime import datetime
from patient.models import Slot

class Command(BaseCommand):
    help = 'Delete slots from the database for a particular date'

    def add_arguments(self, parser):
        parser.add_argument('date', type=str, help='Date in YYYY-MM-DD format')

    def handle(self, *args, **kwargs):
        date_str = kwargs['date']
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            self.stderr.write(self.style.ERROR('Invalid date format. Please use YYYY-MM-DD.'))
            return

        slots_to_delete = Slot.objects.filter(date=date_obj)
        num_deleted, _ = slots_to_delete.delete()

        self.stdout.write(self.style.SUCCESS(f'{num_deleted} slots deleted successfully for {date_str}.'))
