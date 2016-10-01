#! /usr/bin/env python
# -*- coding: utf-8 -*-

import argparse, re, sys, time
from os import path

class CustomAction(argparse.Action):
    def __init__(self, option_strings, dest, help, nargs= None, **keyargs):
        self.text = keyargs['text']
        super(CustomAction, self).__init__(option_strings, dest= dest, help= help, nargs= 0)
    def __call__(self, parser, namespace, values= None, option_strings= None):
        if callable(self.text): self.text()
        else: print(str(self.text))
        parser.exit()

NEWLINE = '\n'
CLEAR = '\r\x1b[2K'
ERROR = CLEAR + '\033[41m\033[97m ERROR \033[0m'
DONE = CLEAR + NEWLINE + '\033[42m\033[97m DONE \033[0m'
PROCESSING = CLEAR + '\033[43m\033[97m PROCESSING \033[0m'
INFO = CLEAR + NEWLINE + '\033[44m\033[97m INFO \033[0m'

def loading(bag, points= 4, interval= 0.5, btxt= PROCESSING, atxt= ''):
    bag['step'] = bag['step'] if 'step' in bag else 0
    bag['time'] = bag['time'] if 'time' in bag else time.time()
    now = time.time()
    if now - bag['time'] > interval:
        bag['time'] = now
        bag['step'] = (bag['step'] + 1) % points
    sys.stdout.write(CLEAR + btxt + '.' * bag['step'] + ' ' * (points - bag['step']) + atxt)
    sys.stdout.flush()
    return bag

def writeout(txt):
    sys.stdout.write(CLEAR + txt)
    sys.stdout.flush()

def parse_int(_str):
    try:
        return int(_str)
    except ValueError:
        return 0

def parse_csv_data(data):
    csv_data_re = re.compile(r'''\s*([^,"']+?|"(?:[^"\\]|\\.)*"|'(?:[^'\\]|\\.)*')\s*(?:,|$)''')
    return csv_data_re.findall(data)

def parse_csv_file(path):
    data = ''
    with open(path) as file:
        data = ''.join(file.readlines())
        data = data.replace('\n', '')
    return parse_csv_data(data= data)

def parse_csv(input):
    csv_path_re = re.compile(r'^\/?\S+\.csv')
    path = csv_path_re.match(input)
    if path == None:
        return parse_csv_data(data= input)
    else:
        return parse_csv_file(path= path.group())

def get_directory_path(_directory):
    if _directory != None:
        _path = path.abspath(_directory)
        if path.isdir(_path):
            return _path
    return

def get_file_path(_file):
    if _file != None:
        _path = path.abspath(_file)
        if path.isfile(_path):
            return _path
    return