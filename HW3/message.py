import sys
import os

class MessageType:
    spam = "spam"
    legit = "legit"
    unknown = "unknown"

class Message:
    __slots__ = ['subject', 'text', 'spam', 'mtype']
    def __init__(self, subject, text, mtype):
        self.subject = subject
        self.text = text
        self.mtype = mtype
    def __str__(self):
        return ("Subject (%s): %s" % (self.mtype, ' '.join(map(str, self.subject))) + '\n\n' + ' '.join(map(str, self.text)))

def parse_message(filename, all):
    subject = list(map(int, all[0].split()[1:]))
    text = list(map(int, ''.join(all[1:]).split()))
    if 'spmsg' in filename:
        mtype = MessageType.spam
    elif 'legit' in filename:
        mtype = MessageType.legit
    else:
        mtype = MessageType.unknown
    return Message(subject, text, mtype)

def read_messages():
    cwd = os.path.dirname(os.path.abspath(__file__))
    ret = []
    for part in os.listdir(cwd + '\\input\\'):
        ret.append([])
        for fn in os.listdir(cwd + '\\input\\' + part):
            with open(cwd + '\\input\\' + part + '\\' + fn, 'r') as f:
                ret[-1].append(parse_message(fn, list(f)))
    return ret
