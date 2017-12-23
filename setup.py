#!/usr/bin/env python

from setuptools import setup

setup(
    name='imeditor',
    version='0.5.2',
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
    packages=['imeditor',
            'imeditor.editor',
            'imeditor.filters',
            'imeditor.interface'],
    package_data = {'imeditor' : ['assets/*.*'] },
    data_files=[('share/pixmaps', ['imeditor/assets/imeditor.png']),
            ('share/applications', ['imeditor.desktop'])],
    entry_points={
        'gui_scripts': [
            'imeditor = imeditor.main:main',
        ]
    },
    install_requires=['Pillow']
)
