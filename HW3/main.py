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
    spamProb = -math.log(mtypes[MessageType.spam]) - sum(math.log(mProb[MessageType.spam, word] + eps) for word in text)
    legitProb = -math.log(mtypes[MessageType.legit]) - sum(math.log(mProb[MessageType.legit, word] + eps) for word in text)
    if spamProb < legitProb * 1.0:
        return MessageType.spam
    else:
        return MessageType.legit

def main():
    mails = read_messages()
    mtypes, mProb = defaultdict(lambda: 0), defaultdict(lambda: 0)
    for pack in mails:
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
    counts = [[0, 0], [0, 0]]
    for pack in mails:
        for msg in pack:
            ptype = classify(mtypes, mProb, all_words, msg)
            predict.append(int(ptype == MessageType.spam))
            answer.append(int(msg.mtype == MessageType.spam))
            counts[ptype == MessageType.spam][msg.mtype == MessageType.spam] += 1
    print("mean squared error: ", mean_squared_error(predict, answer))
    print("f1 score: ", f1_score(predict, answer))
    print("test count: ", sum(len(pack) for pack in mails))
    print("legit message in legit folder: ", counts[0][0])
    print("legit message in spam folder:  ", counts[0][1])
    print("spam message in legit folder:  ", counts[1][0])
    print("spam message in spam folder:   ", counts[1][1])

main()
