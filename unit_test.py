import unittest
from utils import check_if_expected_datetime, convert_datetime_format, send_msg_via_mail
from datetime import datetime, date, time

class TestUtils(unittest.TestCase):
    '''Testing the functions in utils.py'''

    def setUp(self):
        '''Set up testing objects'''
        pass

    def test_convert_datetime_format(self):
        '''Testing convert_datetime_format menthod'''

        self.assertEqual(convert_datetime_format("19/07/2021 at 8:45 AM"), datetime(2021, 7, 19, 8, 45))
        self.assertEqual(convert_datetime_format("19/07/2021 at 8:45 PM"), datetime(2021, 7, 19, 20, 45))
        self.assertEqual(convert_datetime_format("04/06/2021 at 11:25 AM"), datetime(2021, 6, 4, 11, 25))
        self.assertEqual(convert_datetime_format("01/09/2021 at 1:00 PM"), datetime(2021, 9, 1, 13, 00))

    def test_check_if_expected_datetime(self):
        self.assertFalse(check_if_expected_datetime("19/07/2021 at 8:45 AM", date(2021, 5, 28), date(2021, 6, 4), time(9, 0, 0), time(18, 0, 0)))
        self.assertFalse(check_if_expected_datetime("19/07/2021 at 8:45 PM", date(2021, 5, 28), date(2021, 6, 4), time(9, 0, 0), time(18, 0, 0)))
        self.assertTrue(check_if_expected_datetime("04/06/2021 at 11:25 AM", date(2021, 5, 28), date(2021, 6, 4), time(9, 0, 0), time(18, 0, 0)))
        self.assertFalse(check_if_expected_datetime("01/09/2021 at 1:00 PM", date(2021, 5, 28), date(2021, 6, 4), time(9, 0, 0), time(18, 0, 0)))
        
    def test_send_msg_via_mail(self):
        send_msg_via_mail("Hello")

if __name__ == '__main__':
    unittest.main(verbosity=3)