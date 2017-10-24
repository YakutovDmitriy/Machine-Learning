import sys
import os

class Message:
    __slots__ = ['subject', 'text']
    def __init__(self, subject, text):
        self.subject = subject
        self.text = text
    def __str__(self):
        return ("Subject: %s" % ' '.join(self.subject) + '\n\n' + ' '.join(self.text))

def parse_message(all):
    subject = list(map(int, all[0].split()[1:]))
    text = list(map(int, ''.join(all[1:]).split()))
    return Message(subject, text)

def read_messages():
    cwd = os.path.dirname(os.path.abspath(__file__))
    ret = []
    for part in os.listdir(cwd + '\\input\\'):
        ret.append([])
        for fn in os.listdir(cwd + '\\input\\' + part):
            with open(cwd + '\\input\\' + part + '\\' + fn, 'r') as f:
                ret[-1].append(parse_message(list(f)))
    return ret
