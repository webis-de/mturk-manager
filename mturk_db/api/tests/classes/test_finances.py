from django.test import TestCase
from api.models import Batch, HIT


class TestsFinances(TestCase):
    @classmethod
    def setUpTestData(cls):
        batch = Batch.objects.create(name='batch1', use_sandbox=True)


    def test1(self):
        batch = Batch.objects.first()
        self.assertEquals(200, 200)

    def test2(self):
        batch = Batch.objects.first()
        self.assertEquals(200, 200)
