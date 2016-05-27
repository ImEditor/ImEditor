# -*- coding: utf-8 -*-
#!/usr/bin/python3

import pytest
from sys import argv

global path
global args

path = 'imeditor/tests/'
args = '--strict --verbose'

def tests(args=args):
    tests = str()
    if 'file' not in args:
        tests += path + 'tools_test.py'
    tests += args
    errno = pytest.main(tests)
    return errno

if __name__ == '__main__':
    path = ''
    args = list()
    for arg in argv:
        args.append(arg)
    args = ' '.join(args[1:])
    errno = tests(args)
    print('Tests exited with ' + str(errno))
