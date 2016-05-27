# -*- coding: utf-8 -*-
#!/usr/bin/python3

import sys
from setuptools import setup
from setuptools.command.test import test as TestCommand

class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        from imeditor.tests.run_tests import tests
        errno = tests()
        sys.exit(errno)

def read(filename):
    with open(filename, 'r') as myfile:
        return myfile.read().split()

setup(
    name = 'ImEditor',
    version = '0.1',
    author='Nathan Seva, Hugo Posnic',
    tests_require=['pytest'],
    install_requires=read('requirements.txt'),
    cmdclass={'test': PyTest},
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
    ],
    extras_require={
        'testing': ['pytest']
    }
)
