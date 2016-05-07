#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess
import sys

usage = 'Usage: {} pattern path'.format(__file__)
extensions = ('.a', '.o', '.so', '.dylib')

args  = sys.argv
if len(args) != 3:
    print(usage)
    sys.exit(1)

pattern = args[1]
path    = args[2]

for root, dirs, files in os.walk(path):
    for f in files:
        if f.endswith(extensions):
            command = 'nm {} | c++filt | grep {}'.format(os.path.join(root, f), pattern)
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
            
