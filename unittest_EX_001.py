import unittest
from extractor import Extractor
ex = Extractor()


class MyTestCase(unittest.TestCase):
    def test_01_name_have(self):
        self.assertEqual(('刘', '娅', '璇'), ex.extract_name("审核人是刘雅轩"))
        self.assertEqual(('杨', '慧', '宇'), ex.extract_name("是杨惠雨啊"))
        self.assertEqual(('刘', '岳', '涵'), ex.extract_name("我的审核人叫刘月寒"))
        self.assertEqual(('刘', '岳', '涵'), ex.extract_name("审核人是我的主任，刘岳涵"))

    def test_01_name_none(self):
        self.assertEqual(None, ex.extract_name("审核人是张小明"))
        self.assertEqual(None, ex.extract_name("审核人是123458QQQjja"))
        self.assertEqual(None, ex.extract_name(None))


    def test_01_email_none(self):
        self.assertEqual(None, ex.extract_email("抄送邮箱是7889ii.com"))
        self.assertEqual(None, ex.extract_email("抄送给@f11m.com"))
        self.assertEqual(None, ex.extract_email("16527777@tongjieducn，这个是抄送的邮箱"))
        self.assertEqual(None, ex.extract_email(None))
        self.assertEqual(None, ex.extract_email(''))

    def test_01_email_have(self):
        self.assertEqual(['7889@ii.com'], ex.extract_email("抄送邮箱是7889@ii.com"))
        self.assertEqual(['mm_l0182@f11m.com'], ex.extract_email("抄送给mm_l0182@f11m.com"))
        self.assertEqual(['16527777@tongji.edu.cn'], ex.extract_email("16527777@tongji.edu.cn，这个是抄送的邮箱"))
        self.assertEqual(['126@126.c'], ex.extract_email("126@126.c哈哈哈om"))


if __name__ == '__main__':
    unittest.main()
