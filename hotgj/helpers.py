#! /usr/bin/env python
# -*- coding: utf-8 -*-

import argparse

class CustomAction(argparse.Action):
    def __init__(self, option_strings, dest, help, nargs= None, **keyargs):
        self.text = keyargs['text']
        super(CustomAction, self).__init__(option_strings, dest= dest, help= help, nargs= 0)
    def __call__(self, parser, namespace, values= None, option_strings= None):
        print self.text
        parser.exit()

_ERROR = '\033[41m\033[97m ERROR \033[0m'
_DONE = '\033[42m\033[97m DONE \033[0m'
_PROCESSING = '\033[43m\033[97m PROCESSING \033[0m'
_INFO = '\033[44m\033[97m INFO \033[0m'
_CLEAR = '\r\x1b[2K'

def loading(i, num= 8, speed= 0.5, btxt= _PROCESSING, atxt= ''):
    i = (i % num) * speed
    return '\r' + btxt + '.' * i + ' ' * (num * speed - i - (1 if num % 2 == 0 else 0)) + atxt + ' '
