from unittest import TestCase
from my_calendar.utils import check_exist_fields


class TestCheckDictFields(TestCase):

    def setUp(self):
        self.email_passwd = check_exist_fields('email', 'passwd')

    def test_valid(self):
        self.assertTrue(self.email_passwd({'email': 'sdf'}))
        self.assertTrue(self.email_passwd({'passwd': 'sdf'}))
        self.assertTrue(self.email_passwd({'email': 'sdf', 'passwd': 'sdf'}))
        self.assertTrue(self.email_passwd({'email': 'sdf', 'passwd': 'sdf', 'else_field': 'else'}))

    def test_invalid(self):
        self.assertFalse(self.email_passwd({}))
        self.assertFalse(self.email_passwd({'else_field': 'else'}))
