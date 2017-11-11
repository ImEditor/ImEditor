#!/usr/bin/python

import sys
from setuptools import setup

setup(
    name = 'ImEditor',
    version = '0.1.1',
    author='Nathan Seva, Hugo Posnic',
    install_requires=read('requirements.txt'),
    description = ('Simple & versatile image editor.'),
    license = 'GNU GPL v3',
    keywords = 'image editor picture imeditor',
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
