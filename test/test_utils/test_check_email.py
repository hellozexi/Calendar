from unittest import TestCase
from my_calendar.utils import check_email


class TestCheckEmail(TestCase):

    def test_valid(self):
        self.assertTrue(check_email('xua@wustl'))
        self.assertTrue(check_email('xua1234@wuxtl'))
        self.assertTrue(check_email('xua@wustl.edu'))
        self.assertTrue(check_email('x3ua@wuxtl'))
        self.assertTrue(check_email('xua@wuxtl.edg'))
        self.assertTrue(check_email('xua@wuxtl.com'))
        self.assertTrue(check_email('xua@sdfu.net'))
        self.assertTrue(check_email('111111@wuxtl'))

    def test_invalid(self):
        self.assertFalse(check_email('asdfsdfsdfsd'))
        self.assertFalse(check_email('$$$$$$$'))
        self.assertFalse(check_email('wustl@sdf '))
        self.assertFalse(check_email('xua @ wuxtl.edg'))
        self.assertFalse(check_email('xua @wuxtl.edg'))
