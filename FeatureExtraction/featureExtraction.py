# -*- coding: utf-8 -*-
"""
Created on Tue Jul 31 11:44:19 2018
Updated on Mon Sep  2 14:46:57 2019
@author: Nestor Santiago
"""

import csv
import datetime
import os
from fCalculation import tdom, fdom
from statistics import mode
from statistics import StatisticsError
from ftFunctions import createHeader, extractSensor, getTime, features, featureJoiner

#Will run through subjects,activities,and trials inputted
def extraction(d_base_path,features_path,
               n_sub=[1,17],
               n_act=[1,11],
               n_trl=[1,3],
               t_window = ['1&0.5','2&1','3&1.5'],
               t_stamp = False,
               single_f = True):
    for twnd in t_window:
        print(twnd)
        for i  in range(n_sub[0],n_sub[1]+1):
            sub = 'Subject' + str(i)
            print(twnd + '-' + sub)
            for j in range(n_act[0],n_act[1]+1):
                act = 'Activity' + str(j)
                print(twnd+'-'+str(i) + '--' + act)
                for k in range(n_trl[0],n_trl[1]+1):
                    trl = 'Trial' + str(k)
                    subloc = sub+'\\'+act+'\\'
                    path1 = d_base_path+subloc + trl + '\\' + sub+act+trl+'.csv'
                    path2 = features_path + subloc  + trl + '\\' 
                    print('------'+trl+' - '+twnd)
                    features(path1,path2,sub,act,trl,j,twnd,t_stamp)
                    print('---------------------DONE')
        if single_f:
            featureJoiner(features_path,twnd,t_stamp,n_sub,n_act,n_trl)

def main():
    d_base_path = 'DataSet\\'
    features_path = d_base_path
    extraction (d_base_path,features_path)
    print('End of task')
if __name__ == "__main__":
    main()
