#!/usr/bin/python

from setuptools import setup

setup(
    name='ImEditor',
    version='0.2.1',
    description='Simple & versatile image editor.',
    url='https://imeditor.github.io',
    author='Nathan Seva, Hugo Posnic',
    license='GNU GPL v3',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Multimedia :: Graphics :: Editors',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3 :: Only'
    ],
    keywords = 'image editor picture imeditor',
    packages=['imeditor'],
    install_requires=['Pillow']
)
