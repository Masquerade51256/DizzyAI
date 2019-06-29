import unittest
from getType import *


class MyTestCase(unittest.TestCase):
    def test_01_sick(self):
        self.assertEqual("病假", get_type("我想请个病假"))
        self.assertEqual("病假", get_type("我生病了，请个假"))

    def test_01_affair(self):
        self.assertEqual("事假", get_type("我想请个事假"))
        self.assertEqual("事假", get_type("我家里有事，请个假"))

    def test_01_marriage(self):
        self.assertEqual("婚假", get_type("我下周打算结婚，想请个假"))
        self.assertEqual("婚假", get_type("我想请婚假"))

    def test_02_none(self):
        self.assertEqual(None, get_type("请假"))
        self.assertEqual(None, get_type("123458QQQjja"))
        self.assertEqual(None, get_type(None))


if __name__ == '__main__':
    unittest.main()
