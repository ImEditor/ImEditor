#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='imeditor',
    version='0.5.1',
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
    package_dir = {'imeditor' : 'src/imeditor'},
    packages=find_packages(),
    package_data = {'imeditor' : ['assets/*.*'] },
    data_files=[('share/pixmaps', ['src/imeditor/assets/imeditor.png']),
            ('share/applications', ['imeditor.desktop'])],
    entry_points={
        'gui_scripts': [
            'imeditor = imeditor.__main__:main',
        ]
    },
    install_requires=['Pillow']
)
