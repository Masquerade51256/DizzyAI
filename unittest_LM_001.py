import unittest
from getTime import *
from LeaveMessage import LeaveMessage

class MyTestCase(unittest.TestCase):
    def test_01_start_end_dur(self):
        self.assertEqual(('2019-07-03 00:00:00', '2019-07-05 00:00:00', '3 days, 0:00:00'),
                         get_start_and_end_and_duration("我想从今天请到后天，请三天事假", LeaveMessage()))
        self.assertEqual(('2020-03-10 00:00:00', '2020-03-24 00:00:00', '15 days, 0:00:00'),
                         get_start_and_end_and_duration("我想从明年3月10号请到3月24号请15天假去旅游", LeaveMessage()))

    def test_02_start_end_none(self):
        self.assertEqual(('2019-07-03 00:00:00', '2019-07-05 00:00:00', None),
                         get_start_and_end_and_duration("我想从今天请到后天", LeaveMessage()))
        self.assertEqual(('2020-03-10 00:00:00', '2020-03-24 00:00:00', None),
                         get_start_and_end_and_duration("我想从明年3月10号请到3月24号", LeaveMessage()))

    def test_03_start_none_dur(self):
        self.assertEqual(('2019-07-03 09'
                          ':00:00', '2019-07-05 13:00:00', '3 days, 4:00:00'),
                         get_start_and_end_and_duration("我想从今天开始请3天半事假", LeaveMessage()))
        self.assertEqual(('2020-03-10 09:00:00', '2020-03-24 09:00:00', '15 days, 0:00:00'),
                         get_start_and_end_and_duration("我想明年3月10号请15天假去旅游", LeaveMessage()))

    def test_04_start_none_none(self):
        self.assertEqual(('2019-07-05 09:00:00', None, None),
                         get_start_and_end_and_duration("后天我想请假", LeaveMessage()))
        self.assertEqual(('2019-12-25 10:00:00', None, None),
                         get_start_and_end_and_duration("12月25号上午我请假。", LeaveMessage()))

    def test_05_none_none_dur(self):
        self.assertEqual((None, None, '0 days, 4:00:00'),
                         get_start_and_end_and_duration("我打算请半天假", LeaveMessage()))
        self.assertEqual((None, None, '30 days, 0:00:00'),
                         get_start_and_end_and_duration("我想请一个月的假期。", LeaveMessage()))

    def test_06_none_none_none(self):
        self.assertEqual((None, None, None),
                         get_start_and_end_and_duration("我需要请假探亲", LeaveMessage()))
        self.assertEqual((None, None, None),
                         get_start_and_end_and_duration("请假类型是婚假", LeaveMessage()))

    def test_07_conflict(self):
        self.assertEqual((None, None, None),
                         get_start_and_end_and_duration("明天到下周一请8天假", LeaveMessage()))
        self.assertEqual((None, None, None),
                         get_start_and_end_and_duration("明年2月27号到3月1号，请3天假。", LeaveMessage()))

    def test_08_none(self):
        self.assertEqual((None, None, None),
                         get_start_and_end_and_duration(None, LeaveMessage()))
        self.assertEqual((None, None, None),
                         get_start_and_end_and_duration("明年2月27号到3月1号，请3天假。", None))
        self.assertEqual((None, None, None),
                         get_start_and_end_and_duration(None, None))



if __name__ == '__main__':
    unittest.main()
