import unittest
from getReason import get_reason
from stanfordcorenlp import StanfordCoreNLP

nlp = StanfordCoreNLP(r'./stanford-corenlp-full-2018-10-05', lang='zh', memory='2g', quiet=True, )
nlp.parse("test")


class MyTestCase(unittest.TestCase):
    def test_01_reason(self):
        self.assertEqual("带孩子去医院看病 ",
                         get_reason("我想请半天假带孩子去医院看病。", nlp))
        self.assertEqual("我去派出所补办身份证 ",
                         get_reason("我今天上午要去派出所补办身份证，想请半天假。", nlp))
        self.assertEqual("我家里有急事 ",
                         get_reason("我家里有急事，想请假2天。", nlp))

    def test_02_none(self):
        self.assertEqual(None,
                         get_reason("明天请假三天", nlp))
        # self.assertEqual(None,
        #                  get_reason("喂？在吗？", nlp))
        self.assertEqual(None,
                         get_reason("今天到下周一", nlp))
        self.assertEqual(None,
                         get_reason("", nlp))
        self.assertEqual(None,
                         get_reason(None, nlp))



if __name__ == '__main__':
    unittest.main()
