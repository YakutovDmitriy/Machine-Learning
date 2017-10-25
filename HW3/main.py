import os
import sys
import math
import numpy
from message import *
from collections import defaultdict
from sklearn.metrics import f1_score, mean_squared_error

def training(pack):
    mProb, mtypes, wcnt = defaultdict(lambda:0), defaultdict(lambda:0), defaultdict(lambda:0)
    for msg in pack:
        for word in msg.text:
            mProb[msg.mtype, word] += 1
            wcnt[word] += 1
            mtypes[msg.mtype] += 1
    for mtype, word in mProb.keys():
        mProb[mtype, word] /= wcnt[word]
    for mtype in mtypes.keys():
        mtypes[mtype] /= len(pack)
    return mtypes, mProb

def classify(mtypes, mProb, all_words, msg):
    eps = 10 ** -7
    text = list(filter(lambda word: word in all_words, msg.text))
    spamProb = math.log(mtypes[MessageType.spam]) + sum(math.log(mProb[MessageType.spam, word] + eps) for word in text)
    legitProb = math.log(mtypes[MessageType.legit]) + sum(math.log(mProb[MessageType.legit, word] + eps) for word in text)
    if spamProb > legitProb + 10:
        return MessageType.spam
    else:
        return MessageType.legit

def main(mode):
    mails = read_messages()
    if mode == "CROSS":
        tcm = [(mails[:x] + mails[x + 1:], [m]) for x, m in enumerate(mails)]
    elif mode == "ALL":
        tcm = [(mails, mails)]
    else:
        raise RuntimeException("Unknown mode: %s" % mode)
    sum_mse, sum_f1, sum_count = 0, 0, defaultdict(lambda: 0.0)
    for test_mail, check_mail in tcm:
        mtypes, mProb = defaultdict(lambda: 0), defaultdict(lambda: 0)
        for pack in test_mail:
              curc, curf = training(pack)
              for k in curc.keys():
                  mtypes[k] += curc[k]
              for k in curf.keys():
                  mProb[k] += curf[k]
        for k in mtypes.keys():
            mtypes[k] /= len(mails)
        for k in mProb.keys():
            mtypes[k] /= len(mails)
        all_words = set(map(lambda p: p[1], mProb.keys()))
        predict = []
        answer = []
        for pack in check_mail:
            for msg in pack:
                ptype = classify(mtypes, mProb, all_words, msg)
                predict.append(int(ptype == MessageType.spam))
                answer.append(int(msg.mtype == MessageType.spam))
                sum_count[ptype, msg.mtype] += 1
        sum_mse += mean_squared_error(predict, answer)
        sum_f1 += f1_score(predict, answer)
    print("Training in mode %s:" % mode.lower())
    print("  average number of mails in test:", sum(len(x) for x in mails) / len(tcm))
    print("  mean squared error:", sum_mse / len(tcm))
    print("  f1 score:", sum_f1 / len(tcm))
    for predict in [MessageType.spam, MessageType.legit]:
        for actual in [MessageType.spam, MessageType.legit]:
            print("  %s message in %s folder: %f" % (actual, predict, sum_count[predict, actual] / len(tcm)))


main("ALL")
print()
main("CROSS")