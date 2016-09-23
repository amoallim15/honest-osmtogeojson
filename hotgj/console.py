#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import argparse
from helpers import *

CURRENT_VERSION = '0.0.1'
DESC = """
This tool convert large (≳ 100 MB) OpenStreetMaps OSM data in XML format to GeoJSON in one go.
  __  ___  __    __  ___   __  _  _  
 / _)( __)/  \  (  )/ __) /  \( \( ) 
( (/\| _)( () )__)( \__ \( () )  \ | 
 \__/(___)\__/(___/ (___/ \__/(_)\_) 

"""
DEFAULT_IN_MEMORY_DECT_SIZE = '300'
DEFAULT_IN_MEMORY_LIST_LENGTH = '10000000'

parser = argparse.ArgumentParser(description= DESC, formatter_class= argparse.RawTextHelpFormatter)

parser.add_argument(
    'convert',
    help= 'convert OSM data file in XML format to GeoJSON'
)
parser.add_argument(
    '-d',
    '--destination',
    nargs= '?',
    help= 'save GeoJSON data to this file'
)
parser.add_argument(
    '-v',
    '--version',
    action= 'version',
    version= CURRENT_VERSION
)
parser.add_argument(
    '-t',
    '--tags',
    action= CustomAction,
    help= 'show the default uninteresting tags to be skipped',
    text= 'aaa aaa aaa'
)
parser.add_argument(
    '-s',
    '--skip',
    nargs= '?',
    default= True,
    help= 'comma seperated values of uninteresting tags to be skipped, or a csv file path'
)
parser.add_argument(
    '-m',
    '--memory-dect',
    nargs= '?',
    default= DEFAULT_IN_MEMORY_DECT_SIZE,
    help= 'in memory allocation sweet spot in MB to process the OSM data, default '+ DEFAULT_IN_MEMORY_DECT_SIZE +' MB'
)
parser.add_argument(
    '-l',
    '--memory-list',
    nargs= '?',
    default= DEFAULT_IN_MEMORY_LIST_LENGTH,
    help= 'in memory lists length sweet spot to process the OSM data, default '+ DEFAULT_IN_MEMORY_LIST_LENGTH +' elements'
)

def execute(args= sys.argv):
    args = parser.parse_args(args[1:])
    print args
    print 'well done, now we rolling..'
