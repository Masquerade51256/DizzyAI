from random import randint
def get_start_and_end_and_duration(sentence):
	return (None, None, None) if randint(0, 1) == 0 else ("2018-01-02", "2018-01-03", 1)

def get_type(sentence):
	return None if randint(0, 1) == 0 else "事假"

def ask(message):
	if message.startDate is None and message.endDate is not None and message.duration is None:
		return "请输入开始时间"
	elif message.startDate is not None and message.endDate is None and message.duration is None:
		return "你想请几天假"
	elif message.startDate is None and message.endDate is None:
		return "请输入开始时间和结束时间"

	if message.type is None:
		return "请输入请假类型"

def do_ask_for_leave(sentence):
	return "请假" in sentence

def ask_for_leave(sentence):
	from LeaveMessage import LeaveMessage
	message = LeaveMessage()
	while True:
		if message.startDate is None or message.endDate is None:
			message.startDate, message.endDate, message.duration = get_start_and_end_and_duration(sentence)

		if message.type is None:
			message.type = get_type(sentence)

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
			print(message.startDate, message.endDate, message.type)
			break
		print("你要做什么呢")

main()