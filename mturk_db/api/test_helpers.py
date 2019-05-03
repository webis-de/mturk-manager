from api.models import Project, Batch, HIT, Assignment, Settings_Batch
from django.utils import timezone
from api.enums import assignments


def set_up_test_database():
    project = set_up_project(name='project')

    set_up_batch(name='batch1', project=project)
    set_up_batch(name='batch2', project=project)

def set_up_project(name):
    return Project.objects.create(
        version=15,
        name=name,
        slug=name,
    )

def set_up_batch(name, project):
    batch = Batch.objects.create(name=name, use_sandbox=True)

    Settings_Batch.objects.create(
        name='settings_batch_{}'.format(name),
        batch=batch,
        project=project,
        count_assignments=10,
    )

    now = timezone.now()

    list_hits = []
    for index in range(10):
        list_hits.append(HIT.objects.create(
            id_hit='hit_living_{}_{}'.format(name, index),
            batch=batch,
            datetime_expiration=now + timezone.timedelta(days=5 if index < 5 else -5),
            datetime_creation=now,
            count_assignments_dead=index
        ))

    for index, hit in enumerate(list_hits):
        for index1 in range(index):
            status_external = None
            status_internal = None

            if index1 % 5 == 1:
                status_external = assignments.STATUS_EXTERNAL.APPROVED
            elif index1 % 5 == 2:
                status_external = assignments.STATUS_EXTERNAL.REJECTED
            elif index1 % 5 == 3:
                status_external = assignments.STATUS_EXTERNAL.APPROVED
                status_internal = assignments.STATUS_INTERNAL.REJECTED
            elif index1 % 5 == 4:
                status_external = assignments.STATUS_EXTERNAL.REJECTED
                status_internal = assignments.STATUS_INTERNAL.APPROVED

            Assignment.objects.create(
                id_assignment='assignment_{}_{}_{}'.format(name, hit.id_hit, index1),
                hit=hit,
                status_external=status_external,
                status_internal=status_internal,
            )