#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import gc
import shelve
import xml.etree.ElementTree as ET
from os import path, remove
from sys import getsizeof
from contextlib import closing as CL
from helpers import *

DEFAULT_IN_MEMORY_DECT_SIZE = '300'
DEFAULT_IN_MEMORY_LIST_LENGTH = '10000000'
DEFAULT_DB_FILE = 'temp.dat'
DEFAULT_SKIP_TAGS = [
    "source",
    "source_ref",
    "source:ref",
    "history",
    "attribution",
    "created_by",
    "tiger:county",
    "tiger:tlid",
    "tiger:upload_uuid"
]
DEFAULT_META_ATTR = [
    "user",
    "uid",
    "timestamp",
    "visible",
    "changeset"
]
OSM = 'osm'
BOUNDS = 'bounds'
NODE = 'node'
WAY = 'way'
RELATION = 'relation'
TAG = 'tag'
ND = 'nd'
MEMBER = 'member'
OSM_ALL_TAGS = [OSM, BOUNDS, NODE, WAY, RELATION, TAG, ND, MEMBER]
OSM_MAIN_TAGS = [NODE, WAY, RELATION]

class OSMIndexingException(Exception):
    pass

class OSMConvertingException(Exception):
    pass

def reset_db_file(_directory):
    _path = get_file_path(_directory + '/' + DEFAULT_DB_FILE)
    try:
        if _path is not None:
            print _path
            remove(_path)
    except OSError as e:
        raise ConsoleArgumentException(e)
    return

def format_in_db_dict_id(elm):
    return elm.tag + '/' + elm.attrib['id']

def format_in_db_list_id(key, pos):
    return key + '/' + str(pos)

def stream_osm_file(_path):
    stack = []
    for event, element in ET.iterparse(_path, events=('start', 'end')):
        if event == 'start':
            parent = stack[-1] if len(stack) > 0 else None
            stack.append(element)
            yield element, parent
        else:
            stack.pop()
            element.clear()
    return

def deduplicator(objA, objB):
    verA = parse_int(objA['attrib']['version'])
    verB = parse_int(objB['attrib']['version'])
    return objA if verA >= verB else objB

def validate_element():
    return

def index_element(_element, _parent, _dict, _list):
    if _element.tag == OSM and _parent == None:
        _dict[_element.tag] = { 'attrib': dict(_element.attrib) }

    elif _element.tag == BOUNDS and _parent.tag == OSM:
        _dict[_element.tag] = { 'attrib': dict(_element.attrib) }

    elif _element.tag in OSM_MAIN_TAGS and _parent.tag == OSM:
        _element_id = format_in_db_dict_id(_element)
        if _element_id in _dict:
            _dict[_element_id] = deduplicator(_dict[_element_id], { 'attrib': dict(_element.attrib) })
        else:
            _list[_element.tag + 's'].append(_element.attrib['id'])
            _dict[_element_id] = { 'attrib': dict(_element.attrib) }

    elif _element.tag == TAG and _parent.tag in OSM_MAIN_TAGS:
        _parent_id = format_in_db_dict_id(_parent)
        if 'properties' not in _dict[_parent_id]:
            _dict[_parent_id]['properties'] = {}
        _dict[_parent_id]['properties'][_element.attrib['k']] = _element.attrib['v']

    elif _element.tag == ND and _parent.tag == WAY:
        _parent_id = format_in_db_dict_id(_parent)
        if 'nodes' not in _dict[_parent_id]:
            _dict[_parent_id]['nodes'] = []
        _dict[_parent_id]['nodes'].append(_element.attrib['ref'])

    elif _element.tag == MEMBER and _parent.tag == RELATION:
        _parent_id = format_in_db_dict_id(_parent)
        if 'members' not in _dict[_parent_id]:
            _dict[_parent_id]['members'] = []
        _dict[_parent_id]['members'].append(dict(_element.attrib))
    return

def store_to_db(_dict):
    with CL(shelve.open(DEFAULT_DB_PATH, 'c')) as db:
        for key in _dict:
            if key in db:
                temp = deduplicator(db[key], _dict[key])
                db[key] = temp
            else:
                db[key] = _dict[key]
    return

def store_list_to_db(_key, _list, _last):
    with CL(shelve.open(DEFAULT_DB_PATH, 'c')) as db:
        db[_key] = _list
        db['elements-count'] = _last
    return

def index_osm_file(osm_path, in_memory_dict_size, in_memory_list_length):
    osm = stream_osm_file(osm_path)
    in_memory_allowed_size = in_memory_dict_size * 1024 * 1024
    in_memory_allowed_list_length = in_memory_list_length
    in_memory_dict = {}
    in_memory_list = {'nodes': [], 'ways': [], 'relations': []}
    in_memory_list_pos = { 'nodes': 0, 'ways': 0, 'relations': 0 }

    for element, parent in osm:
        if element.tag in OSM_MAIN_TAGS:
            for key in in_memory_list:
                if len(in_memory_list[key]) > in_memory_allowed_list_length:
                    _list_id = format_in_db_list_id(key, in_memory_list_pos[key])
                    store_list_to_db(_key= _list_id, _list= in_memory_list[key], _last= in_memory_list_pos)
                    in_memory_list[key] = []
                    in_memory_list_pos[key] += 1
                    gc.collect()
            if getsizeof(in_memory_dict) > in_memory_allowed_size:
                store_to_db(_dict= _dict)
                in_memory_dict = {}
                gc.collect()
        try:
            # validate_element(element, parent)
            index_element(_element= element, _parent= parent, _dict= in_memory_dict, _list = in_memory_list)
        except OSMIndexingException as e:
            print _ERROR, e

    store_to_db(_dict= in_memory_dict)
    for key in in_memory_list:
        _list_id = format_in_db_list_id(key, in_memory_list_pos[key])
        store_list_to_db(_key= _list_id, _list= in_memory_list[key], _last= in_memory_list_pos)
    return

def convert_osm_file(db_path, skip_tags):

    return


