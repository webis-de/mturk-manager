from django.db.models import F, Value, Count, Q, Sum, IntegerField, ExpressionWrapper, Max, Min
from django.db.models.functions import Coalesce

from api.enums import assignments
from api.models import Account_Mturk, Project, Message_Reject, Batch
from mturk_db.settings import URL_MTURK_SANDBOX
import boto3
from pytz import timezone
from datetime import datetime
from django.utils.text import slugify
from django.conf import settings

class Manager_Projects(object):
    object_account_mturk = None
    # try:
    #     object_account_mturk = Account_Mturk.objects.all()[0]
    #     # object_account_mturk = Account_Mturk.objects.get(name='webis')
    # except Exception:
    #     raise Exception('No credentials for the MTurk account are set')


    @classmethod
    def get_object_account_mturk(cls):
        if cls.object_account_mturk == None:
            try:
                cls.object_account_mturk = Account_Mturk.objects.all()[0]
            except Exception:
                raise Exception('No credentials for the MTurk account are set')

        return cls.object_account_mturk


    @classmethod
    def get_all(cls):
        return Project.objects.all()

    @staticmethod
    def get(database_object_project):
        queryset_batches_sandbox = Batch.objects.filter(
            project=database_object_project,
            use_sandbox=True,
        ).annotate(
            count_hits=Count('hits')
        ).annotate(
            count_assignments_available=Coalesce(Count('hits__assignments', distinct=True), 0),
            count_assignments_total=F('count_hits') * F('settings_batch__count_assignments'),
            count_assignments_approved=Coalesce(Count(
                'hits__assignments',
                distinct=True,
                filter=Q(hits__assignments__status_external=assignments.STATUS_EXTERNAL.APPROVED)
            ), 0),
            count_assignments_rejected=Coalesce(Count(
                'hits__assignments',
                distinct=True,
                filter=Q(hits__assignments__status_external=assignments.STATUS_EXTERNAL.REJECTED)
            ), 0),
        ).annotate(
            costs_max=F('count_assignments_total') * F('settings_batch__reward'),
            costs_so_far=F('count_assignments_approved') * F('settings_batch__reward'),
        ).aggregate(
            sum_costs_max_sandbox=Coalesce(Sum('costs_max'), 0),
            max_costs_max_sandbox=Coalesce(Max('costs_max'), 0),
            min_costs_max_sandbox=Coalesce(Min('costs_max'), 0),

            sum_costs_so_far_sandbox=Coalesce(Sum('costs_so_far'), 0),
            max_costs_so_far_sandbox=Coalesce(Max('costs_so_far'), 0),
            min_costs_so_far_sandbox=Coalesce(Min('costs_so_far'), 0),
        )

        queryset_batches = Batch.objects.filter(
            project=database_object_project,
            use_sandbox=False,
        ).annotate(
            count_hits=Count('hits')
        ).annotate(
            count_assignments_available=Coalesce(Count('hits__assignments', distinct=True), 0),
            count_assignments_total=F('count_hits') * F('settings_batch__count_assignments'),
            count_assignments_approved=Coalesce(Count(
                'hits__assignments',
                distinct=True,
                filter=Q(hits__assignments__status_external=assignments.STATUS_EXTERNAL.APPROVED)
            ), 0),
            count_assignments_rejected=Coalesce(Count(
                'hits__assignments',
                distinct=True,
                filter=Q(hits__assignments__status_external=assignments.STATUS_EXTERNAL.REJECTED)
            ), 0),
        ).annotate(
            costs_max=F('count_assignments_total') * F('settings_batch__reward'),
            costs_so_far=F('count_assignments_approved') * F('settings_batch__reward'),
        ).aggregate(
            sum_costs_max=Coalesce(Sum('costs_max'), 0),
            max_costs_max=Coalesce(Max('costs_max'), 0),
            min_costs_max=Coalesce(Min('costs_max'), 0),

            sum_costs_so_far=Coalesce(Sum('costs_so_far'), 0),
            max_costs_so_far=Coalesce(Max('costs_so_far'), 0),
            min_costs_so_far=Coalesce(Min('costs_so_far'), 0),
        )

        queryset_batches_sandbox.update(queryset_batches)

        queryset = Project.objects.filter(
            pk=database_object_project.pk
        ).annotate(
            **{key: Value(value, output_field=IntegerField()) for key, value in queryset_batches_sandbox.items()}
        ).get()
        # queryset = Batch.objects.filter(
        #     project=database_object_project,
        #     use_sandbox=use_sandbox,
        # ).annotate(
        #     count_hits=Count('hits')
        # ).annotate(
        #     count_assignments_available=Coalesce(Count('hits__assignments', distinct=True), 0),
        #     count_assignments_total=F('count_hits') * F('settings_batch__count_assignments'),
        #     count_assignments_approved=Coalesce(Count(
        #         'hits__assignments',
        #         distinct=True,
        #         filter=Q(hits__assignments__status_external=assignments.STATUS_EXTERNAL.APPROVED)
        #     ), 0),
        #     count_assignments_rejected=Coalesce(Count(
        #         'hits__assignments',
        #         distinct=True,
        #         filter=Q(hits__assignments__status_external=assignments.STATUS_EXTERNAL.REJECTED)
        #     ), 0),
        # ).annotate(
        #     costs_max=F('count_assignments_total') * F('settings_batch__reward'),
        #     costs_so_far=F('count_assignments_approved') * F('settings_batch__reward'),
        # )
        #
        # sort_by = request.query_params.get('sort_by')
        # if sort_by is not None:
        #     descending = request.query_params.get('descending', 'false') == 'true'
        #     queryset = queryset.order_by(
        #         ('-' if descending else '') + sort_by
        #     )
        #
        return queryset

    @classmethod
    def get_mturk_api(cls, use_sandbox=True):
        if use_sandbox:
            return boto3.client('mturk',
                aws_access_key_id=cls.get_object_account_mturk().key_access,
                aws_secret_access_key=cls.get_object_account_mturk().key_secret,
                region_name='us-east-1',
                endpoint_url=URL_MTURK_SANDBOX
            )
        else:
            return boto3.client('mturk',
                aws_access_key_id=cls.get_object_account_mturk().key_access,
                aws_secret_access_key=cls.get_object_account_mturk().key_secret,
                region_name='us-east-1'
            )

    @classmethod
    def check_uniqueness(cls, name):
        return not Project.objects.filter(name=name).exists()

    @classmethod
    def create(cls, data):
        project = Project.objects.create(
            name=data['name'],
            slug=slugify(data['name']),
            fk_account_mturk=cls.get_object_account_mturk(),
            version=settings.VERSION_PROJECT,
        )

        return project

    @staticmethod
    def update(instance, validated_data):
        for key, value in validated_data.items():
            if key == 'message_reject':
                message_reject, was_created = Message_Reject.objects.get_or_create(message_lowercase=value.lower(), defaults={
                    'message': value
                })

                if not was_created:
                    message_reject.message = value
                    message_reject.save()

                instance.message_reject_default = message_reject
                instance.save()
                # messages_reject_deleted = Message_Reject.objects.all().annotate(
                #     count_usage=Count('project')
                # ).filter(count_usage=0).delete()
            else:
                setattr(instance, key, value)

        instance.save()
        return instance

    @classmethod
    def get_count_assignments_max_per_worker(cls, database_object_project):
        project = Project.objects.get(slug=database_object_project.slug)

        return {
            'count_assignments_max_per_worker': project.count_assignments_max_per_worker,
        }

    @classmethod
    def set_count_assignments_max_per_worker(cls, database_object_project, value):
        project = Project.objects.filter(slug=database_object_project.slug).update(
            count_assignments_max_per_worker=value
        )

        return {
            'count_assignments_max_per_worker': value,
        }

    @staticmethod
    def ping(database_object_project):
        now = datetime.now(timezone('Europe/Berlin'))
        database_object_project.datetime_visited = now
        database_object_project.save()
        return { 'datetime': now }

    @staticmethod
    def delete(database_object_project):
        database_object_project.delete()
