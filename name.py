from stanfordcorenlp import StanfordCoreNLP
from pypinyin import lazy_pinyin, Style
import pypinyin


# 输入：审核人名单（一个列表），一句话。
# 输出：如果匹配到，返回匹配的名字（一个元组）；如果没匹配到，返回0；

class NameMatcher:
    Auditor = ['刘岳涵', '徐锦程', '倪奕玮', '刘娅璇', '刘雨', '杨慧宇', '苏昭帆', '郭辉', '邹笑寒', '杜庆峰', '赵冬月']

    def __init__(self):
        self.nlp = StanfordCoreNLP(r'./stanford-corenlp-full-2018-02-27', lang='zh')
        return

    def match(self, sentence):
        result = self.name_match(self.Auditor, sentence)
        if result == 0:
            return None
        else:
            return result

    def close(self):
        self.nlp.close()

    def auditor_transform(self, chinese_auditor_nameList):
        pinyin_auditor_nameList = []
        for chinese_auditor_name in chinese_auditor_nameList:
            pinyin_auditor_name = tuple(lazy_pinyin(chinese_auditor_name))
            chinese_name = tuple(chinese_auditor_name)
            pinyin_auditor_name = pinyin_auditor_name + chinese_name
            pinyin_auditor_nameList.append(pinyin_auditor_name)
        # print(pinyin_auditor_nameList)
        return pinyin_auditor_nameList

    def employer_transform(self, sentence):
        sentence_list = self.nlp.ner(sentence)
        chinese_employer_nameList = []
        for nameEntity in sentence_list:
            if nameEntity[1] == 'PERSON':
                chinese_employer_nameList.append(nameEntity[0])
        pinyin_employer_nameList = []
        for chinese_employer_name in chinese_employer_nameList:
            pinyin_employer_name = tuple(lazy_pinyin(chinese_employer_name))
            pinyin_employer_nameList.append(pinyin_employer_name)

        # print(pinyin_employer_nameList)
        return pinyin_employer_nameList

    def minDistance(self, words1, words2):
        m = len(words1)
        n = len(words2)
        if m == 0:
            return n
        if n == 0:
            return m
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(1, m + 1): dp[i][0] = i
        for j in range(1, n + 1): dp[0][j] = j
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
                        # 我的print(distance)
                    if distance < len(employer):
                        return auditor[len(employer):]
        return 0
