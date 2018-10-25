from unittest import TestCase
from my_calendar.utils import check_word


class TestCheckEmail(TestCase):

    def test_valid(self):
        self.assertTrue(check_word('prepare dinner'))
        self.assertTrue(check_word('this is my word'))
        self.assertTrue(check_word('do you like it'))
        self.assertTrue(check_word('find the 1st issue'))

    def test_invalid(self):
        self.assertFalse(check_word("''''''''''''''"))
        self.assertFalse(check_word('"""""""""""""""'))
        self.assertFalse(check_word('^%&^%()(**('))
