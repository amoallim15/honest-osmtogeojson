#! /usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import re
from os import path

class CustomAction(argparse.Action):
    def __init__(self, option_strings, dest, help, nargs= None, **keyargs):
        self.text = keyargs['text']
        super(CustomAction, self).__init__(option_strings, dest= dest, help= help, nargs= 0)
    def __call__(self, parser, namespace, values= None, option_strings= None):
        print self.text
        parser.exit()

ERROR = '\033[41m\033[97m ERROR \033[0m'
DONE = '\033[42m\033[97m DONE \033[0m'
PROCESSING = '\033[43m\033[97m PROCESSING \033[0m'
INFO = '\033[44m\033[97m INFO \033[0m'
CLEAR = '\r\x1b[2K'

def loading(i, num= 8, speed= 0.5, btxt= PROCESSING, atxt= ''):
    i = (i % num) * speed
    return '\r' + btxt + '.' * i + ' ' * (num * speed - i - (1 if num % 2 == 0 else 0)) + atxt + ' '

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

def get_directory_path(_directory= ''):
    _path = path.abspath(_directory)
    if path.isdir(_path):
        return _path
    else:
        return None

def get_file_path(_file= ''):
    _path = path.abspath(_file)
    if path.isfile(_path):
        return _path
    else:
        return None

