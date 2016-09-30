#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import gc
import sys
import shelve
import xml.etree.ElementTree as ET
from os import path, remove
from sys import getsizeof
from contextlib import closing as CL
from helpers import *

DEFAULT_IN_MEMORY_SIZE = '300'
DEFAULT_DB_FILE = 'temp.dat'
DEFAULT_SKIP_TAGS = [
    'source',
    'source_ref',
    'source:ref',
    'history',
    'attribution',
    'created_by',
    'tiger:county',
    'tiger:tlid',
    'tiger:upload_uuid'
]
DEFAULT_META_ATTR = [
    'user',
    'uid',
    'timestamp',
    'visible',
    'changeset'
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
DEFAULT_ELEMENT_HANDLERS = []

class OSMIndexingException(Exception): pass
class OSMConvertingException(Exception): pass
class DBAccessException(Exception): pass

def get_element_handlers():
    return DEFAULT_ELEMENT_HANDLERS

def get_db_file(_directory):
    return path.abspath(_directory +'/'+ DEFAULT_DB_FILE)

def reset_db_file(_directory):
    _path = get_file_path(_directory +'/'+ DEFAULT_DB_FILE)
    try:
        if _path is not None:
            remove(_path)
    except OSError as e:
        raise DBAccessException(e)
    return

def update_db_file(_directory, func):
    _path = get_db_file(_directory= _directory), 'c')
    try:
        with CL(shelve.open(_path, 'c')) as db:
            if callable(func):
                func(db= db)
    except IOError as e:
        raise DBAccessException('db access error: '+ DEFAULT_DB_FILE +', details: ' + e)
    return

def store_dect_to_db(_directory, _dict):
    def func(db):
        for key in _dict:
            if key in db:
                temp = deduplicator(db[key])
                db[key] = temp
            else:
                db[key] = _dict[key]
    update_db_file(_directory= _directory, func= func)

def store_list_to_db(_directory, _list, _pos):
    def func(db):
        for key in _list:
            list_id = format_in_db_list_id(key, _pos[key])
            db[list_id] = _list[key]
            _list[key] = []
            _pos[key] += 1
        db['elements-count'] = _pos
    update_db_file(_directory= _directory, func= func)

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

def is_same_version(objA, prt):
    verA = parse_int(objA['attrib']['version'])
    verB = parse_int(prt.attrib['version'])
    return True if verA == verB else False

def OSM_handler(elm, prt, _dict):
    if elm.tag == OSM and prt == None:
        _dict['osm'] = { 'attrib': _dict(elm.attrib) }
        return True

def BOUNDS_handler(elm, prt, _dict):
    if prt == None: return
    if elm.tag == BOUNDS and prt.tag == OSM:
        _dict['bounds'] = { 'attrib': _dict(elm.attrib) }
        return True

def OSM_MAIN_TAGS_handler(elm, prt, _dict):
    if prt == None: return
    if elm.tag in OSM_MAIN_TAGS and prt.tag == OSM:
        elm_id = format_in_db_dict_id(elm)
        if elm_id in _dict:
            _dict[elm_id] = deduplicator(_dict[elm_id], { 'attrib': dict(elm.attrib) })
        else:
            _list[elm.tag + 's'].append(elm.attrib['id'])
            _dict[elm_id] = { 'attrib': dict(elm.attrib) }
        return True

def TAG_handler(elm, prt, _dict):
    # validator
    if prt == None: return
    # processing
    if elm.tag == TAG and prt.tag in OSM_MAIN_TAGS:
        prt_id = format_in_db_dict_id(prt)
        if is_same_version(_dict[prt_id], prt):
            if 'properties' not in _dict[prt_id]:
                _dict[prt_id]['properties'] = {}
            _dict[prt_id]['properties'][elm.attrib['k']] = elm.attrib['v']
        return True

def ND_handler(elm, prt, _dict):
    if prt == None: return
    if elm.tag == ND and prt.tag == WAY:
        prt_id = format_in_db_dict_id(prt)
        if 'nodes' not in _dict[prt_id]:
            _dict[prt_id]['nodes'] = []
        _dict[prt_id]['nodes'].append(elm.attrib['ref'])
        return True

def MEMBER_handler(elm, prt, _dict):
    if prt == None: return
    if elm.tag == MEMBER and prt.tag == RELATION:
        prt_id = format_in_db_dict_id(prt)
        if 'members' not in _dict[prt_id]:
            _dict[prt_id]['members'] = []
        _dict[prt_id]['members'].append(dict(elm.attrib))
        return True

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

def index_osm_file(osm_path, destination, in_memory_dict_size):
    osm = stream_osm_file(osm_path)
    in_memory_allowed_size = in_memory_dict_size * 1024 * 1024
    in_memory_dict = {}
    in_memory_list = {'nodes': [], 'ways': [], 'relations': []}
    in_memory_list_pos = { 'nodes': 0, 'ways': 0, 'relations': 0 }
    step = 0

    for element, parent in osm:
        if element.tag in OSM_MAIN_TAGS:
            if getsizeof(in_memory_dict) > in_memory_allowed_size:
                store_list_to_db(_directory= destination, _list= in_memory_list, _pos= in_memory_list_pos)
                store_dect_to_db(_directory= destination, _dict= _dict)
                in_memory_dict = {}
                gc.collect()
        try:
            element_handlers = get_element_handlers()
            consumed = None
            for key in element_handlers:
                if callable(element_handlers[key]):
                    consumed = element_handlers(element, parent, _dict)
            if consumed == None:
                raise OSMIndexingException('unidentified element, element ignored: '+ element)
            index_element(_element= element, _parent= parent, _dict= in_memory_dict, _list= in_memory_list)
            step = loading(i= step, x= 60, y= 15)
        except OSMIndexingException as e:
            print(ERROR, e)

    print(CLEAR)
    print(PROCESSING, 'finalising indexing, please wait..')

    store_list_to_db(_directory= destination, in_memory_list= in_memory_list, in_memory_list_pos= in_memory_list_pos)
    store_dect_to_db(_directory= destination, _dict= in_memory_dict)
    return

def convert_osm_file(db_path, skip_tags):
    return


