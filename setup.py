#!/usr/bin/python

import sys
from setuptools import setup

setup(
    name = 'ImEditor',
    version = '0.1',
    author='Nathan Seva, Hugo Posnic',
    install_requires=read('requirements.txt'),
    description = ('Éditeur de photos, simple & polyvalent'),
    license = 'GNU GPL v3',
    keywords = 'photo editor picture imeditor',
    url = 'https://imeditor.github.io/',
    packages=['imeditor'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Topic :: Multimedia :: Graphics :: Editors',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only'
    ]
)
