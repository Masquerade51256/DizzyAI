import re


def do_ask_for_leave(sentence):
    try:
        match_obj = re.search(r'(.*)请(.*)假(.*).*', sentence, re.M | re.I)
        if match_obj:
            return True
        else:
            return False
    except:
        return False

do_ask_for_leave("请假去看病")