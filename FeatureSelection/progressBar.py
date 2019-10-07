# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 23:04:33 2019
@author: JosePablo
Base code taken from Nils Kohlmey's stack overflow contribution:
https://stackoverflow.com/questions/6169217/replace-console-output-in-python
"""

import sys

def progressBar(name, value, endvalue, bar_length = 50, width = 1):
        percent = float(value) / endvalue
        progress = '|' * int(round(percent*bar_length))
        remaining = '-' * (bar_length - len(progress))
        sys.stdout.write("\r{0: <{1}}: [{2}]{3}%".format(\
                         name, width, progress + remaining, int(round(percent*100))))
        sys.stdout.flush()
        if value == endvalue:        
             sys.stdout.write('\n')