#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys, argparse, pkg_resources, time
from hotgj.helpers import *
from hotgj.core import *

class ConsoleArgumentException(Exception): pass

CURRENT_VERSION = '0.0.1'
DESC = """
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

def print_default_skip_tags():
    print(INFO, 'Default Skip Tags:')
    print('------------------------------')
    print('  skip values:     ', (NEWLINE +'                    ').join(DEFAULT_SKIP_TAGS), NEWLINE)

parser = argparse.ArgumentParser(description= DESC, formatter_class= argparse.RawTextHelpFormatter)
parser.add_argument('convert', help= 'convert OSM data file in XML format to GeoJSON')
parser.add_argument('-d', '--destination', nargs= '?', help= 'process and save the GeoJSON data to this directory')
parser.add_argument('-v', '--version', action= 'version', version= CURRENT_VERSION)
parser.add_argument('-t', '--tags', action= CustomAction, help= 'show the default uninteresting tags to be skipped', text= print_default_skip_tags)
parser.add_argument('-s', '--skip', nargs= '?', default= True, help= 'comma seperated values of uninteresting tags to be skipped, or a csv file path')
parser.add_argument('-m', '--memory', nargs= '?', default= DEFAULT_IN_MEMORY_SIZE, help= 'in memory allocation sweet spot in MB to process the OSM data, default '+ DEFAULT_IN_MEMORY_SIZE +' MB')

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
    raise ConsoleArgumentException('in memory allocation value is too low: '+ temp +' MB')

def destination_value_handler(value):
    _path = get_directory_path(value)
    if _path is not None:
        return _path
    raise ConsoleArgumentException('No such directory exists as a destination: '+ str(value))

def convert_value_handler(value):
    _path = get_file_path(value)
    if _path is not None:
        return _path
    raise ConsoleArgumentException('no such file exists: '+ str(value))

def print_args(args):
    print(INFO, 'Converting Arguments:')
    print('------------------------------')
    print('  convert:         ', args['convert'])
    print('  destination:     ', args['destination'])
    print('  memory:          ', args['memory'], 'MB')
    print('  skip values:     ', (NEWLINE +'                   ').join(args['skip'].split(',')), NEWLINE)

def print_indexing_result(_directory, process_time):
    def func(db):
        osm = db['osm'] if 'osm' in db else None
        bounds = db['bounds'] if 'bounds' in db else None
        print(INFO, 'Indexing Result:')
        print('------------------------------')
        print('  Info:            ', osm)
        print('  Bounds:          ', bounds)
        print('  Processing Time: ', time.strftime('%H:%M:%S', time.gmtime(process_time)), NEWLINE)
    update_db_file(_directory, func)

def execute(args= sys.argv):
    args = vars(parser.parse_args(args[1:]))

    try:
        args['convert'] = convert_value_handler(value= args['convert'])
        args['skip'] = skip_value_handler(value= args['skip'])
        args['memory'] = memory_dect_value_handler(value= args['memory'])
        args['destination'] = destination_value_handler(value= args['destination'])

        print_args(args)
        reset_db_file(args['destination'])
        indexing_time_start = time.time()
        index_osm_file(osm_path= args['convert'], destination= args['destination'], in_memory_dict_size= args['memory'])
        indexing_time_end = time.time()
        print_indexing_result(args['destination'], indexing_time_end - indexing_time_start)

    except (ConsoleArgumentException, DBAccessException) as e:
        print(ERROR, e, NEWLINE)

    


