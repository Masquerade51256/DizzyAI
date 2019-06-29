from extractor import Extractor
import LeaveMessage
import re
from getTime import *
from getType import *
from ask import *
from stanfordcorenlp import StanfordCoreNLP
from getReason import get_reason
ex = Extractor()


# def get_type(sentence):
#     affairs = re.search(r'(.*)事(.*)假(.*).*', sentence, re.M | re.I)
#     sick = re.search(r'(.*)病(.*)假(.*).*', sentence, re.M | re.I)
#     marriage = re.search(r'(.*)婚(.*)假(.*).*', sentence, re.M | re.I)
#     if affairs:
#         return "事假"
#     elif sick:
#         return "病假"
#     elif marriage:
#         return "婚假"
#     else:
#         return None


def ask(message):
    if message.startDate is None and message.endDate is None and message.duration is None and message.type is None and message.examinePerson is None and message.email is None and message.reason is None:
        return "请输入请假时间等信息"

    if message.type is None:
        return "请输入请假类型"

    if message.startDate is None and message.endDate is None and message.duration is None:
        return "请输入请假时间"
    elif message.startDate is not None and message.endDate is None and message.duration is None:
        return "你想请几天假"
    elif message.startDate is None and message.endDate is None:
        return "请输入请假的开始时间"

    if message.examinePerson is None:
        return "请输入您的审批人姓名"

    if message.email is None:
        return "请输入抄送邮箱"

    if message.reason is None:
        print("请输入请假理由")
        message.reason = input()

    return None


# def do_ask_for_leave(sentence):
#     match_obj = re.search(r'(.*)请(.*)假(.*).*', sentence, re.M | re.I)
#     return match_obj


def ask_for_leave(sentence, message):
    while True:
        if message.type is None:
            message.type = get_type(sentence)

        if message.startDate is None or message.endDate is None:
            message.startDate, message.endDate, message.duration = get_start_and_end_and_duration(sentence, message)

        if message.examinePerson is None:
            message.examinePerson = ex.extract_name(sentence)

        if message.email is None:
            message.email = ex.extract_email(sentence)

        if message.reason is None:
            message.reason = get_reason(sentence, nlp)

        question = ask(message)
        if question is not None:
            print(question)
            sentence = input()
            continue

        print("确认吗？")
        sentence = input()
        deny = re.search(r'不|重(新?)(.*)(填(写?)|输(入?))|重来|打?填?写?错了?|改', sentence)
        if deny:
            message.duration = None
            message.type = None
            message.email = None
            message.endDate = None
            message.examinePerson = None
            message.startDate = None
            message.reason = None
            print("请假信息已清空，请重新输入请假内容")
            sentence = input()
        elif "确认" in sentence:
            break
    return message


def main():
    while True:
        print("你要做什么呢")
        sentence = input()
        if do_ask_for_leave(sentence):
            message = ask_for_leave(sentence, LeaveMessage())
            print("\n开始时间：", message.startDate,
                  "\n结束时间：", message.endDate,
                  "\n请假长度：", message.duration,
                  "\n请假类型：", message.type,
                  "\n审核人：", message.examinePerson,
                  "\n抄送邮箱：", message.email,
                  "\n请假理由：", message.reason)
            print("---------------")
            # break

# with StanfordCoreNLP(r'./stanford-corenlp-full-2018-10-05', lang='zh', memory='2g', quiet=True, ) as nlp:
#         nlp.parse("test")
#         main()
