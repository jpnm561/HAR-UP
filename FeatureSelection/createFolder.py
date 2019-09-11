# -*- coding: utf-8 -*-
"""
Created on Sat Aug 24 13:17:03 2019

@author: JosePablo
"""
import os

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('An error ocurred while creating direcory: "' +  directory +'"')