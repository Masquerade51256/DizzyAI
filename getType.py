import re


def get_type(sentence):
    try:
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
    except:
        return None
