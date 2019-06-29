import unittest
from doAskForLeave import *


class MyTestCase(unittest.TestCase):
    def test_01(self):
        self.assertEqual(True, do_ask_for_leave("我家里有事，想请个假回老家"))
        self.assertEqual(True, do_ask_for_leave("我需要请3天假，陪孩子考试"))
        self.assertEqual(True, do_ask_for_leave("我身体不舒服，需要请假"))

    def test_02(self):
        self.assertEqual(False, do_ask_for_leave("喂，你好"))
        self.assertEqual(False, do_ask_for_leave("我的工号是7722"))
        self.assertEqual(False, do_ask_for_leave("在吗？听得到吗?"))
        self.assertEqual(False, do_ask_for_leave(None))


if __name__ == '__main__':
    unittest.main()
