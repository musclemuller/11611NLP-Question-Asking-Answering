# -*- coding: utf-8 -*-
import re


def isMathc(src, pat):
    pattern = re.compile(pat)
    result = re.match(pattern, src)
    if result == None:
        return 0
    else:
        return 1


def chargeType(character):
    # character, number and space
    type_num = ['[a-z]|[A-Z]', '\d', '\s', '\n']
    if isMathc(character, type_num[0]) == 1:
        return 1
    elif isMathc(character, type_num[1]) == 1:
        return 2
    elif isMathc(character, type_num[2]) == 1:
        return 3
    else:
        return 4


def getCharNum(str):
    count = []
    for i in range(4):
        count.append(0)
    #print(len(count))
    for i in range(len(str)):
        if chargeType(str[i]) == 1:
            count[0] += 1
        elif chargeType(str[i]) == 2:
            count[1] += 1
        elif chargeType(str[i]) == 3:
            count[2] += 1
        else:
            count[3] += 1
    return count


if __name__ == "__main__":
    str = 'asc ss./ 124'
    print(getCharNum(str))
