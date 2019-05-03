from django.test import TestCase
from api.classes import Manager_Batches
from api.models import Batch
from api.test_helpers import set_up_test_database


class TestsBatches(TestCase):
    @classmethod
    def setUpTestData(cls):
        set_up_test_database()

    def test_annotate_assignments(self):
        queryset = Batch.objects.all()
        queryset = Manager_Batches.annotate_assignments(queryset)
        batch = queryset.filter(name='batch1').get()

        self.assertEqual(batch.count_hits, 10)

        self.assertEqual(batch.count_assignments_total, 100)
        self.assertEqual(batch.count_assignments_approved, 18)
        self.assertEqual(batch.count_assignments_rejected, 14)
        self.assertEqual(batch.count_assignments_submitted, 13)
        self.assertEqual(batch.count_assignments_dead, 45)

        self.assertEqual(batch.count_assignments_living_total, 50)
        self.assertEqual(batch.count_assignments_living_available, 10)

        self.assertEqual(batch.count_assignments_pending, 40)

    def test_normalize_answer(self):
        pass