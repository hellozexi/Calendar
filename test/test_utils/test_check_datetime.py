from unittest import TestCase
from datetime import datetime
from my_calendar.utils import check_datetime


class TestCheckDateTime(TestCase):
    def test_valid(self):
        # javascript Date ISO format
        self.assertTrue(check_datetime('2018-10-21T20:02:57.296Z'))
        self.assertTrue(check_datetime('2018-10-21 20:02:57.296Z'))
        self.assertTrue(check_datetime('2018 10 21 20:02:57.296Z'))
        self.assertTrue(check_datetime('2018:10:21 20:02:57.296Z'))
        # python datetime format
        self.assertTrue(check_datetime(datetime.now().isoformat()))
        self.assertTrue(check_datetime(str(datetime.now())))

    def test_invalid(self):
        self.assertFalse(check_datetime('1082:20:10 8-10-55'))
        self.assertFalse(check_datetime('201810:21T20:02:57.296Z'))
        self.assertFalse(check_datetime('2018:10:21 20-02-57.296Z'))
        self.assertFalse(check_datetime('xua @ wuxtl.edg'))
        self.assertFalse(check_datetime('xua @wuxtl.edg'))
