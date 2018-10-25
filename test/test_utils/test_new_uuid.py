from unittest import TestCase
from my_calendar.utils import new_uuid


class TestUewUUid(TestCase):

    def test_len(self):
        self.assertEqual(len(new_uuid()), 32)
        self.assertEqual(len(new_uuid()), 32)
        self.assertEqual(len(new_uuid()), 32)

    def test_type(self):
        self.assertEqual(type(new_uuid()), str)

    def test_bar(self):
        self.assertFalse('-' in new_uuid())

    def test_diff(self):
        diff = set([new_uuid() for _ in range(10)])
        self.assertEqual(len(diff), 10)
