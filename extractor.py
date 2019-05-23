import re
from itertools import groupby
import jieba
import jieba.posseg as pseg
from pypinyin import lazy_pinyin, Style

import logging

jieba.setLogLevel(logging.INFO)


class Extractor:
    Aditor = []

    def __init__(self):
        # fp = open('./resource/myDict.dict', 'r')
        with open('./resource/myDict.dict', 'r', encoding='UTF-8') as fp:
            s = fp.readline()
            while s:
                dict = s.split(' ')
                name = dict[0]
                self.Aditor.append(name)
                s = fp.readline()
            # print(self.Aditor)
            fp.close()

        jieba.load_userdict('./resource/myDict.dict')
        return

    def extract_email(self, text):
        if text == '':
            return None
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

    def replace_chinese(self, text):
        if text == '':
            return []
        filtrate = re.compile(u'[\u4E00-\u9FA5]')
        text_without_chinese = filtrate.sub(r' ', text)
        return text_without_chinese

    def replace_ids(self, text):
        if text == '':
            return []
        eng_texts = self.replace_chinese(text)
        sep = ',!?:; ：，.。！？《》、|\\/abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        eng_split_texts = [''.join(g) for k, g in groupby(eng_texts, sep.__contains__) if not k]
        eng_split_texts_clean = [ele for ele in eng_split_texts if len(ele) == 18]

        id_pattern = r'^[1-9][0-7]\d{4}((19\d{2}(0[13-9]|1[012])(0[1-9]|[12]\d|30))|(19\d{2}(0[13578]|1[02])31)|(19\d{2}02(0[1-9]|1\d|2[0-8]))|(19([13579][26]|[2468][048]|0[48])0229))\d{3}(\d|X|x)?$'
        ids = []
        for eng_text in eng_split_texts_clean:
            result = re.match(id_pattern, eng_text, flags=0)
            if result:
                ids.append(result.string)

        for phone_num in ids:
            text = text.replace(phone_num, '')
        return text

    def extract_name(self, text):
        result = self.name_match(self.Aditor, text)
        if result == 0:
            return None
        else:
            return result

    @staticmethod
    def aditor_transform(chinese_aditor_nameList):
        pinyin_aditor_nameList = []
        for chinese_aditor_name in chinese_aditor_nameList:
            pinyin_aditor_name = tuple(lazy_pinyin(chinese_aditor_name))
            chinese_name = tuple(chinese_aditor_name)
            pinyin_aditor_name = pinyin_aditor_name + chinese_name
            pinyin_aditor_nameList.append(pinyin_aditor_name)
        # print(pinyin_aditor_nameList)
        return pinyin_aditor_nameList

    @staticmethod
    def employer_transform(text):
        seg_list = [(str(t.word), str(t.flag)) for t in pseg.cut(text)]
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

    def name_match(self, aditor_list, employer_sentence):
        aditors = self.aditor_transform(aditor_list)
        employers = self.employer_transform(employer_sentence)
        for aditor in aditors:
            for employer in employers:
                # print("jin ru  shuang xun huan")
                # print(len(aditor))
                # print(len(employer))
                if (len(aditor) / 2) != len(employer):
                    # print("name bu deng chang")
                    continue
                else:
                    distance = 0
                    for index in range(0, len(employer)):
                        distance = distance + self.minDistance(aditor[index], employer[index])
                        # print(distance)
                    if distance < len(employer):
                        return aditor[len(employer):]
        return 0

    def most_common(self, content_list):
        if content_list is []:
            return None
        if len(content_list) == 0:
            return None
        return max(set(content_list), key=content_list.count)
