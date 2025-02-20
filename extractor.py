import re
from itertools import groupby
import jieba
import jieba.posseg as posSeg
from pypinyin import lazy_pinyin

import logging

jieba.setLogLevel(logging.INFO)


# noinspection PyTypeChecker
class Extractor:
    Auditor = []

    def __init__(self):
        # fp = open('./resource/myDict.dict', 'r')
        with open('./resource/myDict.dict', 'r', encoding='UTF-8') as fp:
            s = fp.readline()
            while s:
                dict = s.split(' ')
                name = dict[0]
                self.Auditor.append(name)
                s = fp.readline()
            # print(self.Auditor)
            fp.close()

        jieba.load_userdict('./resource/myDict.dict')
        return

    def extract_email(self, text):
        try:
            eng_texts = self.replace_chinese(text)
            eng_texts = eng_texts.replace(' at ', '@').replace(' dot ', '.')
            sep = ',!?:; ，。！？《》、|\\/'
            eng_split_texts = [''.join(g) for k, g in groupby(eng_texts, sep.__contains__) if not k]

            email_pattern = r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z_-]+)+$'

            emails = []
            for eng_text in eng_split_texts:
                result = re.match(email_pattern, eng_text, flags=0)
                if result:
                    emails.append(result.string)
            if len(emails) == 0:
                return None
            else:
                return emails
        except:
            return None

    def replace_chinese(self, text):
        if text == '':
            return []
        filtrate = re.compile(u'[\u4E00-\u9FA5]')
        text_without_chinese = filtrate.sub(r' ', text)
        return text_without_chinese

    def extract_name(self, text):
        try:
            result = self.name_match(self.Auditor, text)
            if result == 0:
                return None
            else:
                return result
        except:
            return None

    @staticmethod
    def auditor_transform(chinese_auditor_nameList):
        pinyin_auditor_nameList = []
        for chinese_auditor_name in chinese_auditor_nameList:
            pinyin_auditor_name = tuple(lazy_pinyin(chinese_auditor_name))
            chinese_name = tuple(chinese_auditor_name)
            pinyin_auditor_name = pinyin_auditor_name + chinese_name
            pinyin_auditor_nameList.append(pinyin_auditor_name)
        # print(pinyin_auditor_nameList)
        return pinyin_auditor_nameList

    @staticmethod
    def employer_transform(text):
        seg_list = [(str(t.word), str(t.flag)) for t in posSeg.cut(text)]
        names = []
        for ele_tup in seg_list:
            if 'nr' in ele_tup[1]:
                names.append(ele_tup[0])

        pinyin_nameList = []
        for name in names:
            pinyin_name = tuple(lazy_pinyin(name))
            pinyin_nameList.append(pinyin_name)
        # print(pinyin_nameList)
        return pinyin_nameList

    @staticmethod
    def minDistance(words1, words2):
        m = len(words1)
        n = len(words2)
        if m == 0:
            return n
        if n == 0:
            return m
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(1, m + 1):
            dp[i][0] = i
        for j in range(1, n + 1):
            dp[0][j] = j
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if words1[i - 1] == words2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    dp[i][j] = min(dp[i - 1][j - 1] + 1, dp[i][j - 1] + 1, dp[i - 1][j] + 1)
        # print(dp)
        # print(dp[m][n])
        return dp[m][n]

    def name_match(self, auditor_list, employer_sentence):
        auditors = self.auditor_transform(auditor_list)
        employers = self.employer_transform(employer_sentence)
        for auditor in auditors:
            for employer in employers:
                # print(len(auditor))
                # print(len(employer))
                if (len(auditor) / 2) != len(employer):
                    # print("name bu deng chang")
                    continue
                else:
                    distance = 0
                    for index in range(0, len(employer)):
                        distance = distance + self.minDistance(auditor[index], employer[index])
                        # print(distance)
                    if distance < len(employer):
                        return auditor[len(employer):]
        return 0
