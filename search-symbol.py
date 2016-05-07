#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
import subprocess
import sys

parser = argparse.ArgumentParser(description='This script is ...')
parser.add_argument('-d', '--demangle', action='store_true', default=False,
                    help='print demangled symbol name if this flag is set (default: False)',)
parser.add_argument('-e', '--extensions', action='store', nargs='+', const=None,
                    default=['a', 'o', 'so', 'dylib'], type=str, choices=None,
                    help='extensions of files for searching target (default: a, o, so, dylib)',
                    metavar=None)
parser.add_argument('pattern', action='store', nargs=None, const=None,
                    default=None, type=str, choices=None,
                    help='symbol name matching pattern',
                    metavar=None)
parser.add_argument('path', action='store', nargs=None, const=None,
                    default=None, type=str, choices=None,
                    help='root path for searching recursively',
                    metavar=None)

args            = parser.parse_args()
commands        = []

def check_command(c):
    ret = subprocess.call(
        'which {} > /dev/null'.format(c),
        shell = True)
    if ret == 0:
        return True
    else:
        return False

if check_command('nm'):
    commands.append('nm {}')

if check_command('readelf'):
    commands.append('readelf -sW {}')

if args.demangle:
    if check_command('c++filt'):
        commands = map(lambda c:c + '| c++filt', commands)
    else:
        print 'require c++filt command'
        exit(1)

if len(commands) == 0:
    print 'require nm or readelf command'
    exit(1)

args.extensions = map(lambda e:'.' + e, args.extensions)

for root, dirs, files in os.walk(args.path):
    for f in files:
        if f.endswith(tuple(args.extensions)):
            for c in commands:
                command = (c + '| grep {}').format(os.path.join(root, f), args.pattern)
                proc = subprocess.Popen(
                    command,
                    shell  = True,
                    stdin  = subprocess.PIPE,
                    stdout = subprocess.PIPE,
                    stderr = subprocess.PIPE)
                stdout_data, stderr_data = proc.communicate()
                if stdout_data != '':
                    print os.path.join(root, f)
                    print stdout_data
                    break
