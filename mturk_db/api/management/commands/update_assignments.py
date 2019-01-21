from django.core.management.base import BaseCommand
from django.db.models import Q

from api.classes import Manager_Projects
from api.models import Account_Mturk, Assignment


class Command(BaseCommand):
    help = 'Update Assignments'
    def handle(self, *args, **options):

        if Account_Mturk.objects.count() != 1:
            raise Exception('Invalid number of mturk accounts')

        count_false = self.update_assignments(False)
        count_true = self.update_assignments(True)

        self.stdout.write(self.style.SUCCESS('Successfully updated assignments ({} real, {} sandbox)'.format(count_false, count_true)))

    def update_assignments(self, use_sandbox):
        self.stdout.write('{}'.format(use_sandbox))
        mturk_api = Manager_Projects.get_mturk_api(use_sandbox)
        print(mturk_api)

        count = 0
        for index, assignment_db in enumerate(Assignment.objects.filter(hit__batch__use_sandbox=use_sandbox).filter(Q(datetime_submit=None) | Q(datetime_accept=None))):
            assignment_mturk = mturk_api.get_assignment(AssignmentId=assignment_db.id_assignment)['Assignment']

            assignment_db.datetime_accept = assignment_mturk['AcceptTime']
            assignment_db.datetime_submit = assignment_mturk['SubmitTime']
            assignment_db.save()
            count += 1
            if index % 100 == 0:
                self.stdout.write('{}'.format(index))

        return count