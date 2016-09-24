#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import argparse
from helpers import *
from core import *
import pkg_resources

class ConsoleArgumentException(Exception):
    pass

_CURRENT_VERSION = '0.0.1'
_DESC = """
This is a python package that converts large (≳ 100 MB) OSM data represented in (XML format) into a GeoJSON data represented in (JSON) in one go.
      _  _  __  _  _  ___  ___  ____    __   ___  __  __  
     ( )( )/  \( \( )( __)/ __)(_  _)  /  \ / __)(  \/  ) 
     | __ ( () )  \ || _) \__ \  )(   ( () )\__ \ )    (  
     (_)(_)\__/(_)\_)(___)(___/ (__)   \__/ (___/(_/\/\_) 
        ____  __     __  ___  __    __  ___   __  _  _    
       (_  _)/  \   / _)( __)/  \  (  )/ __) /  \( \( )   
         )( ( () ) ( (/\| _)( () )__)( \__ \( () )  \ |   
        (__) \__/   \__/(___)\__/(___/ (___/ \__/(_)\_)   
"""

parser = argparse.ArgumentParser(description= _DESC, formatter_class= argparse.RawTextHelpFormatter)

parser.add_argument(
    'convert',
    help= 'convert OSM data file in XML format to GeoJSON'
)
parser.add_argument(
    '-d',
    '--destination',
    nargs= '?',
    help= 'process and save the GeoJSON data to this directory'
)
parser.add_argument(
    '-v',
    '--version',
    action= 'version',
    version= _CURRENT_VERSION
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
    help= 'in memory lists length sweet spot to process the OSM data, default '+ DEFAULT_IN_MEMORY_LIST_LENGTH +' values'
)

def skip_value_handler(value):
    if value == True:
        temp = DEFAULT_SKIP_TAGS
    elif value == None:
        temp = []
    else:
        temp = parse_csv(input= value)
    return ', '.join(temp) or None

def memory_dect_value_handler(value):
    temp = parse_int(value)
    if temp >= 100:
        return temp
    else:
        raise ConsoleArgumentException('in memory allocation value is too low: ' + temp + ' MB')

def memory_list_value_handler(value):
    temp = parse_int(value)
    if temp >= 100000:
        return temp
    else:
        raise ConsoleArgumentException('in memory lists length is too low: ' + temp + ' values')

def destination_value_handler(value):
    _path = get_directory_path(value)
    if _path is not None:
        return _path
    else:
        raise ConsoleArgumentException('No such directory exists: ' + str(value))

def convert_value_handler(value):
    _path = get_file_path(value)
    if _path is not None:
        return _path
    else:
        raise ConsoleArgumentException('no such file exists: ' + str(value))

def execute(args= sys.argv):
    args = vars(parser.parse_args(args[1:]))

    try:
        args['convert'] = convert_value_handler(value= args['convert'])
        args['skip'] = skip_value_handler(value= args['skip'])
        args['memory_dect'] = memory_dect_value_handler(value= args['memory_dect'])
        args['memory_list'] = memory_list_value_handler(value= args['memory_list'])
        args['destination'] = destination_value_handler(value= args['destination'])

        print args
        reset_db_file(args['destination'])
        # index_osm_file(osm_path= args['convert'], in_memory_dict_size= args['memor-dect'], in_memory_list_length= args['memory-list'])
    except ConsoleArgumentException as e:
        print ERROR, e

    





