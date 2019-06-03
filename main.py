from TimeNLP import TimeNormalizer
from extractor import Extractor
from LeaveMessage import LeaveMessage
# from name import NameMatcher
import re
import arrow
import json
from stanfordcorenlp import StanfordCoreNLP
from get_reason import get_reason



message = LeaveMessage()
# nm = NameMatcher()
tn = TimeNormalizer()
ex = Extractor()


# 一天工作时间为8小时
WORK_HOURS = 8

# 上下班时间
GO_WORK_TIME = "09:00:00"
OFF_WORK_TIME = "17:00:00"

def get_start_and_end_and_duration(sentence):
    s_time = message.startDate
    e_time = message.endDate
    duration = message.duration
    pos, res_union = tn.parse(target=sentence)
    # print(pos)
    # print(res)
    # res_union = json.loads(res_union)
    if len(res_union):
        for res in res_union:
            try:
                # print(res)
                if res['type'] == "timedelta":
                    duration = res['timedelta']
                    # print(duration)

                elif res['type'] == "timespan":
                    s_time = res['timespan'][0]
                    e_time = res['timespan'][1]
                elif res['type'] == "timestamp":
                    s_time = res['timestamp']
                    s_hour = str(s_time).split(' ')[1].split(':')[0]
                    # print(s_hour)
                    if s_hour == "00":
                        s_time = str(s_time).split(' ')[0] + ' ' + GO_WORK_TIME
                        # print(s_time)
                    # print(s_time)
            except:
                duration = duration
                s_time = s_time
                e_time = e_time

    a_half_day = re.search(r'(.*)(半)(.*)([天]|[日](.*))', sentence, re.M | re.I)
    more_half_day = re.search(r'((.*)([天]|[日])半(.*))|((.*)(再|还|另外|另)(.*)(加?)半(.*)([天]|[日])(.*))', sentence,
                              re.M | re.I)
    # 类似"一天半"
    if more_half_day:
        # print("more")
        duration = duration.split(', ')[0] + ', ' + str(int(WORK_HOURS / 2)) + ":00:00"
        message.duration = duration
    # "半天"
    elif a_half_day:
        # print("a")
        duration = "0 days, " + str(int(WORK_HOURS / 2)) + ":00:00"
        message.duration = duration

    if s_time is not None and duration is not None:
        t_days = int(duration.split()[0])
        # t_days -= 1
        # print(duration)
        t_hours = duration.split(', ')[1]
        t_hours = int(t_hours.split(':')[0])

        # 未填入结束时间
        if e_time is None:
            e_time = s_time
            e_time = arrow.get(e_time).shift(days=+t_days).format('YYYY-MM-DD HH:mm:ss')
            e_time = arrow.get(e_time).shift(hours=+t_hours).format('YYYY-MM-DD HH:mm:ss')

        # 结束时间矛盾
        elif e_time != arrow.get(s_time).shift(days=+t_days).format('YYYY-MM-DD HH:mm:ss'):
            s_time = None
            e_time = None
            duration = None
            print("输入的请假时间矛盾，已清空")
    return (s_time, e_time, duration)




def get_type(sentence):
    affairs = re.search(r'(.*)事(.*)假(.*).*', sentence, re.M | re.I)
    sick = re.search(r'(.*)病(.*)假(.*).*', sentence, re.M | re.I)
    marriage = re.search(r'(.*)婚(.*)假(.*).*', sentence, re.M | re.I)
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
    if message.startDate is None and message.endDate is None and message.duration is None and message.type is None and message.examinePerson is None and message.email is None and message.reason is None:
        return "请输入请假内容"

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

    if message.reason is None:
        return  "请输入请假理由"

    return None


def do_ask_for_leave(sentence):
    matchObj = re.search(r'(.*)请(.*)假(.*).*', sentence, re.M | re.I)
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
            sentence = ''
        elif "确认" in sentence:
            break
    return message


def main():
        while True:
            print("你要做什么呢")
            sentence = input()
            if do_ask_for_leave(sentence):
                message = ask_for_leave(sentence)
                print("\n开始时间：", message.startDate,
                      "\n结束时间：", message.endDate,
                      "\n请假长度：", message.duration,
                      "\n请假类型：", message.type,
                      "\n审核人：", message.examinePerson,
                      "\n抄送邮箱：", message.email,
                      "\n请假理由：", message.reason)
                break


with StanfordCoreNLP(r'stanford-corenlp-full-2018-10-05', lang='zh', memory='4g', quiet=True, ) as nlp:
        nlp.parse("test")
        main()
