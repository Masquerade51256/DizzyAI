from TimeNormalizer import TimeNormalizer


tn = TimeNormalizer()

s = input()

while s:
    res = tn.parse(target=s)
    print(res)
    s = input()
