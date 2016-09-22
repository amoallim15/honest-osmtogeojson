#! /usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
from os import path



setup(
    name= 'honest-osmtogeojson',
    version= '1.0.0',
    description= 'honest-osmtogeojson is a python module that converts OSM data represented in (XML format) into a GeoJSON data represented in (JSON), inspired by the JavaScript module osmtogeojson.',
    url= 'https://github.com/AXJ15/honest-osmtogeojson',
    author= 'Ali Moallim',
    author_email= 'axj.159@gmail.com',
    license= 'None',
    keywords= 'osm geojson converter honest',
    packages= ['hotgj'],
    entry_points= { 'console_scripts': ['honest-osmtogeojson = hotgj:main'] },
    license= 'MIT',
    classifiers= [
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License'
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)