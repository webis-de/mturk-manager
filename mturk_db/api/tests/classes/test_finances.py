from django.test import TestCase, tag
from api.models import Batch, HIT, Assignment, Project
from api.test_helpers import set_up_test_database
from api.classes import ManagerFinances


class TestsFinances(TestCase):
    @classmethod
    def setUpTestData(cls):
        set_up_test_database()

    def test_aggregate_batches(self):
        queryset_all = Batch.objects.all()

        queryset_empty = queryset_all.filter(name='')
        self.assertEqual(queryset_empty.count(), 0)
        queryset_batch1 = queryset_all.filter(name='batch1')
        queryset_batch2 = queryset_all.filter(name='batch2')

        result_empty = ManagerFinances.aggregate_batches(queryset_empty)

        self.assertEqual(result_empty['sum_costs_approved'], 0)
        self.assertEqual(result_empty['sum_costs_rejected'], 0)
        self.assertEqual(result_empty['sum_costs_submitted'], 0)
        self.assertEqual(result_empty['sum_costs_dead'], 0)
        self.assertEqual(result_empty['sum_costs_pending'], 0)

        result_batch1 = ManagerFinances.aggregate_batches(queryset_batch1)

        self.assertEqual(result_batch1['sum_costs_approved'], 900)
        self.assertEqual(result_batch1['sum_costs_rejected'], 700)
        self.assertEqual(result_batch1['sum_costs_submitted'], 650)
        self.assertEqual(result_batch1['sum_costs_dead'], 2250)
        self.assertEqual(result_batch1['sum_costs_pending'], 2000)

        result_batch2 = ManagerFinances.aggregate_batches(queryset_batch2)

        self.assertEqual(result_batch2['sum_costs_approved'], 1800)
        self.assertEqual(result_batch2['sum_costs_rejected'], 1400)
        self.assertEqual(result_batch2['sum_costs_submitted'], 1300)
        self.assertEqual(result_batch2['sum_costs_dead'], 4500)
        self.assertEqual(result_batch2['sum_costs_pending'], 4000)

        result = ManagerFinances.aggregate_batches(queryset_all)

        self.assertEqual(
            result['sum_costs_approved'],
            result_batch1['sum_costs_approved'] + result_batch2['sum_costs_approved']
        )
        self.assertEqual(
            result['sum_costs_rejected'],
            result_batch1['sum_costs_rejected'] + result_batch2['sum_costs_rejected']
        )
        self.assertEqual(
            result['sum_costs_submitted'],
            result_batch1['sum_costs_submitted'] + result_batch2['sum_costs_submitted']
        )
        self.assertEqual(
            result['sum_costs_dead'],
            result_batch1['sum_costs_dead'] + result_batch2['sum_costs_dead']
        )
        self.assertEqual(
            result['sum_costs_pending'],
            result_batch1['sum_costs_pending'] + result_batch2['sum_costs_pending']
        )

    def test_aggregate_hits(self):
        queryset_all = HIT.objects.all()

        queryset_empty = queryset_all.filter(id_hit='-1')
        self.assertEqual(queryset_empty.count(), 0)
        queryset_batch1 = queryset_all.filter(batch__name='batch1')
        queryset_batch2 = queryset_all.filter(batch__name='batch2')

        result_empty = ManagerFinances.aggregate_hits(queryset_empty)

        self.assertEqual(result_empty['sum_costs_approved'], 0)
        self.assertEqual(result_empty['sum_costs_rejected'], 0)
        self.assertEqual(result_empty['sum_costs_submitted'], 0)
        self.assertEqual(result_empty['sum_costs_dead'], 0)
        self.assertEqual(result_empty['sum_costs_pending'], 0)

        result_batch1 = ManagerFinances.aggregate_hits(queryset_batch1)

        self.assertEqual(result_batch1['sum_costs_approved'], 900)
        self.assertEqual(result_batch1['sum_costs_rejected'], 700)
        self.assertEqual(result_batch1['sum_costs_submitted'], 650)
        self.assertEqual(result_batch1['sum_costs_dead'], 2250)
        self.assertEqual(result_batch1['sum_costs_pending'], 2000)

        result_batch2 = ManagerFinances.aggregate_hits(queryset_batch2)

        self.assertEqual(result_batch2['sum_costs_approved'], 1800)
        self.assertEqual(result_batch2['sum_costs_rejected'], 1400)
        self.assertEqual(result_batch2['sum_costs_submitted'], 1300)
        self.assertEqual(result_batch2['sum_costs_dead'], 4500)
        self.assertEqual(result_batch2['sum_costs_pending'], 4000)

        result = ManagerFinances.aggregate_hits(queryset_all)

        self.assertEqual(
            result['sum_costs_approved'],
            result_batch1['sum_costs_approved'] + result_batch2['sum_costs_approved']
        )
        self.assertEqual(
            result['sum_costs_rejected'],
            result_batch1['sum_costs_rejected'] + result_batch2['sum_costs_rejected']
        )
        self.assertEqual(
            result['sum_costs_submitted'],
            result_batch1['sum_costs_submitted'] + result_batch2['sum_costs_submitted']
        )
        self.assertEqual(
            result['sum_costs_dead'],
            result_batch1['sum_costs_dead'] + result_batch2['sum_costs_dead']
        )
        self.assertEqual(
            result['sum_costs_pending'],
            result_batch1['sum_costs_pending'] + result_batch2['sum_costs_pending']
        )

    def test_aggregate_assignments(self):
        queryset_all = Assignment.objects.all()

        queryset_empty = queryset_all.filter(id_assignment='-1')
        self.assertEqual(queryset_empty.count(), 0)
        queryset_batch1 = queryset_all.filter(hit__batch__name='batch1')
        queryset_batch2 = queryset_all.filter(hit__batch__name='batch2')

        result_empty = ManagerFinances.aggregate_assignments(queryset_empty)

        self.assertEqual(result_empty['sum_costs_approved'], 0)
        self.assertEqual(result_empty['sum_costs_rejected'], 0)
        self.assertEqual(result_empty['sum_costs_submitted'], 0)

        result_batch1 = ManagerFinances.aggregate_assignments(queryset_batch1)

        self.assertEqual(result_batch1['sum_costs_approved'], 900)
        self.assertEqual(result_batch1['sum_costs_rejected'], 700)
        self.assertEqual(result_batch1['sum_costs_submitted'], 650)

        result_batch2 = ManagerFinances.aggregate_assignments(queryset_batch2)

        self.assertEqual(result_batch2['sum_costs_approved'], 1800)
        self.assertEqual(result_batch2['sum_costs_rejected'], 1400)
        self.assertEqual(result_batch2['sum_costs_submitted'], 1300)

        result = ManagerFinances.aggregate_assignments(queryset_all)

        self.assertEqual(
            result['sum_costs_approved'],
            result_batch1['sum_costs_approved'] + result_batch2['sum_costs_approved']
        )
        self.assertEqual(
            result['sum_costs_rejected'],
            result_batch1['sum_costs_rejected'] + result_batch2['sum_costs_rejected']
        )
        self.assertEqual(
            result['sum_costs_submitted'],
            result_batch1['sum_costs_submitted'] + result_batch2['sum_costs_submitted']
        )

    @tag('mturk')
    def test_get_balance(self):
        balance = ManagerFinances.get_balance(True)
