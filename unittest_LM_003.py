import unittest
from main import *
from LeaveMessage import LeaveMessage


class MyTestCase(unittest.TestCase):
    def test_01(self):
        self.assertEqual("请输入请假时间等信息", ask(LeaveMessage()))

    def test_02(self):
        leave_message = LeaveMessage()
        leave_message.type = None
        leave_message.startDate = '2019-06-29 00:00:00'
        self.assertEqual("请输入请假类型", ask(leave_message))

    def test_03(self):
        leave_message = LeaveMessage()
        leave_message.type = "事假"
        self.assertEqual("请输入请假时间", ask(leave_message))

    def test_04(self):
        leave_message = LeaveMessage()
        leave_message.type = "事假"
        leave_message.startDate = '2019-06-29 00:00:00'
        self.assertEqual("你想请几天假", ask(leave_message))

    def test_05(self):
        leave_message = LeaveMessage()
        leave_message.type = "事假"
        leave_message.duration = '3 days, 0:00:00'
        self.assertEqual("请输入请假的开始时间", ask(leave_message))

    def test_06(self):
        leave_message = LeaveMessage()
        leave_message.type = "事假"
        leave_message.startDate = '2019-06-29 00:00:00'
        leave_message.endDate = '2019-07-01 00:00:00'
        leave_message.duration = None
        leave_message.examinePerson = None
        self.assertEqual("请输入您的审批人姓名", ask(leave_message))

    def test_07(self):
        leave_message = LeaveMessage()
        leave_message.type = "事假"
        leave_message.startDate = '2019-06-29 00:00:00'
        leave_message.endDate = '2019-07-01 00:00:00'
        leave_message.duration = None
        leave_message.examinePerson = ('刘', '娅', '璇')
        leave_message.email = None
        self.assertEqual("请输入抄送邮箱", ask(leave_message))


if __name__ == '__main__':
    unittest.main()
