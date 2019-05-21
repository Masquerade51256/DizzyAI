from TimeNLP import TimeNormalizer
from extractor import Extractor
from LeaveMessage import LeaveMessage
# from name import NameMatcher
import re
import arrow
import json

message = LeaveMessage()
# nm = NameMatcher()
tn = TimeNormalizer()
ex = Extractor()

def get_start_and_end_and_duration(sentence):
    s_time = message.startDate
    e_time = message.endDate
    duration = message.duration
    pos, res = tn.parse(target=sentence)
    # print(pos)
    # print(res)
    res = json.loads(res)

    try:
        if res['type'] == "timedelta":
            duration = res['timedelta']
            # print(duration)

        elif res['type'] == "timespan":
            s_time = res['timespan'][0]
            e_time = res['timespan'][1]
        elif res['type'] == "timestamp":
            s_time = res['timestamp']

        if s_time is not None and duration is not None:
            t_days = int(duration.split()[1])
            t_days -= 1

            # t_hours = arrow.get(duration.split(', ')[0], 'H:mm:ss')

            e_time = arrow.get(s_time).shift(days=+t_days).format('YYYY-MM-DD HH:mm:ss')

        return (s_time, e_time, duration)
    except:
        return (s_time, e_time, duration)


def get_type(sentence):
    affairs = re.search(r'(.*)事(.*?)假(.*).*', sentence, re.M | re.I)
    sick = re.search(r'(.*)病(.*?)假(.*).*', sentence, re.M | re.I)
    marriage = re.search(r'(.*)婚(.*?)假(.*).*', sentence, re.M | re.I)
    if affairs:
        return "事假"
    elif sick:
        return "病假"
    elif marriage:
        return "婚假"
    else:
        return None

def get_examinPerson(sentence):
    name = ex.extract_name(sentence)
    # name = nm.match(sentence)
    # print(name)
    return name

def get_email(sentence):
    email = ex.extract_email(sentence)
    return email

def ask(message):
    if message.type is None:
        return "请输入请假类型"

    if message.startDate is None and message.endDate is None and message.duration is None:
        return "请输入请假时间"
    elif message.startDate is not None and message.endDate is None and message.duration is None:
        return "你想请几天假"
    elif message.startDate is None and message.endDate is None:
        return "请输入请假的开始或结束时间"

    if message.examinePerson is None:
        return "请输入您的审批人姓名"

    if message.email is None:
        return "请输入抄送邮箱"

    return None



def do_ask_for_leave(sentence):
    matchObj = re.search(r'(.*)请(.*?)假(.*).*', sentence, re.M | re.I)
    return matchObj


def ask_for_leave(sentence):
    while True:
        if message.type is None:
            message.type = get_type(sentence)

        if message.startDate is None or message.endDate is None:
            message.startDate, message.endDate, message.duration = get_start_and_end_and_duration(sentence)

        if message.examinePerson is None:
            message.examinePerson = get_examinPerson(sentence)

        if message.email is None:
            message.email = get_email(sentence)

        question = ask(message)
        if question is not None:
            print(question)
            sentence = input()
            continue

        print("确认吗？")
        sentence = input()
        if "确认" in sentence:
            break
    return message


def main():
    while True:
        sentence = input()
        if do_ask_for_leave(sentence):
            message = ask_for_leave(sentence)
            print("\n开始时间：", message.startDate,
                  "\n结束时间：", message.endDate,
                  "\n请假长度：", message.duration,
                  "\n请假类型：", message.type,
                  "\n审核人：", message.examinePerson,
                  "\n抄送邮箱：", message.email)
            break
        print("你要做什么呢")


main()
