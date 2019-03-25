from django.core.management.base import BaseCommand
from django.db.models.functions import Lower, Upper

from api.models import Account_Mturk, Worker, Assignment_Worker, Project, Settings_Batch, Template, Template_Worker, Template_Assignment, Template_HIT, Template_Global, Batch, HIT, Assignment


class Command(BaseCommand):
    help = 'Upper-/Lowercases all names'

    def handle(self, *args, **options):
        Account_Mturk.objects.update(
            name=Lower('name')
        )
        self.stdout.write(self.style.SUCCESS('Lowercased Account_Mturk'))

        Batch.objects.update(
            name=Upper('name')
        )
        self.stdout.write(self.style.SUCCESS('Uppercased Batch'))

        HIT.objects.update(
            id_hit=Upper('id_hit')
        )
        self.stdout.write(self.style.SUCCESS('Uppercased HIT'))

        Assignment.objects.update(
            id_assignment=Upper('id_assignment')
        )
        self.stdout.write(self.style.SUCCESS('Uppercased Assignment'))

        Worker.objects.update(
            id_worker=Upper('id_worker')
        )
        self.stdout.write(self.style.SUCCESS('Uppercased Worker'))

        Assignment_Worker.objects.update(
            id_worker=Upper('id_worker'),
            id_assignment=Upper('id_assignment')
        )
        self.stdout.write(self.style.SUCCESS('Uppercased Assignment_Worker'))
