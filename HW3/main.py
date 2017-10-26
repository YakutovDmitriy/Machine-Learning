import os
import sys
import math
import numpy
from message import *
from collections import defaultdict
from sklearn.metrics import f1_score, mean_squared_error
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib import collections as mc
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

def training(pack):
    mProb, mtypes, wcnt = [defaultdict(lambda:0) for _ in range(3)]
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



def classify(mtypes, mProb, all_words, msg, spam_weight):
    eps = 10 ** -7
    text = list(filter(lambda word: word in all_words, msg.text))
    spamProb = math.log(mtypes[MessageType.spam]) + sum(math.log(mProb[MessageType.spam, word] + eps) for word in text)
    legitProb = math.log(mtypes[MessageType.legit]) + sum(math.log(mProb[MessageType.legit, word] + eps) for word in text)
    res = MessageType.spam if spamProb > legitProb * spam_weight else MessageType.legit
    return res

def main(mails, mode, spam_weights):
    if mode == "CROSS":
        tcm = [(mails[:x] + mails[x + 1:], [m]) for x, m in enumerate(mails)]
    elif mode == "ALL":
        tcm = [(mails, mails)]
    else:
        raise RuntimeException("Unknown mode: %s" % mode)
    sum_mse, sum_f1, sum_count = defaultdict(lambda: 0), defaultdict(lambda: 0), defaultdict(lambda: defaultdict(lambda: 0.0))
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
        for spam_weight in spam_weights:
            for pack in check_mail:
                for msg in pack:
                    ptype = classify(mtypes, mProb, all_words, msg, spam_weight)
                    predict.append(int(ptype == MessageType.spam))
                    answer.append(int(msg.mtype == MessageType.spam))
                    sum_count[spam_weight][ptype, msg.mtype] += 1
            sum_mse[spam_weight] += mean_squared_error(predict, answer)
            sum_f1[spam_weight] += f1_score(predict, answer)
    for spam_weight in spam_weights:
        print("Training in mode %s (spam weight %f):" % (mode.lower(), spam_weight))
        print("  average number of mails in test:", sum(len(x) for x in mails) / len(tcm))
        print("  mean squared error:", sum_mse[spam_weight] / len(tcm))
        print("  f1 score:", sum_f1[spam_weight] / len(tcm))
        for predict in [MessageType.spam, MessageType.legit]:
            for actual in [MessageType.spam, MessageType.legit]:
                print("  %s message in %s folder: %f" % (actual, predict, sum_count[spam_weight][predict, actual] / len(tcm)))
    return [(sum_count[w][MessageType.legit, MessageType.spam] /
                (sum_count[w][MessageType.spam, MessageType.spam] + sum_count[w][MessageType.legit, MessageType.spam]),
            sum_count[w][MessageType.legit, MessageType.legit] /
                (sum_count[w][MessageType.spam, MessageType.legit] + sum_count[w][MessageType.legit, MessageType.legit]))
            for w in spam_weights]

def build_plot(points):
    cmap_bold = ListedColormap(['#000000', '#ffffff'])
    plt.figure()
    plt.rcParams["figure.figsize"] = list(map(lambda x: x * 1, plt.rcParams["figure.figsize"]))
    points = sorted(points)
    data = sum(
        [[(points[i][0], points[i + 1][0]), (points[i][1], points[i + 1][1]), 'b'] for i in range(len(points) - 1)], []
    )
    plt.plot(*data)
    for xx, yy in points:
        plt.scatter(xx, yy, c='r',cmap=cmap_bold, linewidths=0, s=5)
    plt.title("ROC-curve")
    plt.xlim(0, max(p[0] for p in points) * 1.1)
    plt.ylim(0, max(p[1] for p in points) * 1.1)
    plt.show()

mails = read_messages()

# points = main(mails, "CROSS", [1.1, 1.8])
# build_plot(points)

for mode in ["CROSS"]:
    points = main(mails, mode, list(numpy.arange(0.05, 3.05, 0.05)))
    print(points)
    build_plot(points)
