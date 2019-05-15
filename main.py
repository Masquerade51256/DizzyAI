from TimeNormalizer import TimeNormalizer
from cocoNLP.extractor import extractor
from LeaveMessage import LeaveMessage
import re
import json

message = LeaveMessage()

tn = TimeNormalizer()
ex = extractor()

def get_start_and_end_and_duration(sentence):
    s_time = message.startDate
    e_time = message.endDate
    duration = message.duration
    res = json.loads(tn.parse(target=sentence))
    # print(res)
    try:
        if res['type'] == "timedelta":
            duration = res['timedelta']
        elif res['type'] == "timespan":
            s_time = res['timespan'][0]
            e_time = res['timespan'][1]
        elif res['type'] == "timestamp":
            s_time = res['timestamp']
        return (s_time, e_time, duration)
    except:
        return (s_time, e_time, duration)


def get_type(sentence):
    affairs = re.search(r'(.*)事(.*?)假(.*).*', sentence, re.M | re.I)
    sick = re.search(r'(.*)病(.*?)假(.*).*', sentence, re.M | re.I)
    if affairs:
        return "事假"
    elif sick:
        return "病假"
    else:
        return None

def get_examinPerson(sentence):
    name = ex.extract_name(sentence)
    # print(name)
    return name


def ask(message):
    if message.type is None:
        return "请输入请假类型"

    if message.startDate is None and message.endDate is None and message.duration is None:
        return "请输入请假时间"
    elif message.startDate is not None and message.endDate is None and message.duration is None:
        return "你想请几天假"
    elif message.startDate is None and message.endDate is None:
        return "请输入请假的开始或结束时间"

    while message.examinePerson is None:
        print("请输入您的审批人姓名")
        sentence = input()
        message.examinePerson = get_examinPerson(sentence)
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
            print(message.startDate, message.endDate, message.duration, message.type, message.examinePerson)
            break
        print("你要做什么呢")


main()
