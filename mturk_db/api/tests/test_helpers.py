from django.test import TestCase

from api.helpers import mturk_status_to_database_status, database_status_to_mturk_status, keep_fields
from api.enums import assignments
from api.serializers import Serializer_Assignment


class TestsHelpers(TestCase):
    def test_mturk_status_to_database_status(self):
        self.assertIsNone(mturk_status_to_database_status('Submitted'))
        self.assertEqual(mturk_status_to_database_status('Approved'), assignments.STATUS_EXTERNAL.APPROVED)
        self.assertEqual(mturk_status_to_database_status('Rejected'), assignments.STATUS_EXTERNAL.REJECTED)

        with self.assertRaises(ValueError):
            mturk_status_to_database_status('Wrong Status')

    def test_database_status_to_mturk_status(self):
        self.assertEqual(database_status_to_mturk_status(None), 'Submitted')
        self.assertEqual(database_status_to_mturk_status(assignments.STATUS_EXTERNAL.APPROVED), 'Approved')
        self.assertEqual(database_status_to_mturk_status(assignments.STATUS_EXTERNAL.REJECTED), 'Rejected')

        with self.assertRaises(ValueError):
            database_status_to_mturk_status(3)

    def test_keep_fields(self):
        serializer = Serializer_Assignment()

        keep_fields(serializer, ['id_assignment', 'duration', 'UNKNOWN_FIELD'])

        self.assertEqual(len(serializer.fields), 2)
        self.assertIsNotNone(serializer.fields.get('id_assignment'))
        self.assertIsNotNone(serializer.fields.get('duration'))

        self.assertIsNone(serializer.fields.get('UNKNOWN_FIELD'))
        self.assertIsNone(serializer.fields.get('hit'))


