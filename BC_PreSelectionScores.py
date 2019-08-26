# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 18:01:23 2019

@author: José Pablo
"""

import numpy as np
import os
from sklearn import metrics as met

#an array with the time-windows that will be used
fldr = ['1&0.5', '2&1', '3&1.5']
#an array with the 'experiments' that will be performed
concept = ['IMU','Head','IR_Vision']

for cnpt in concept:
    print(cnpt)
    #This will be performed for all the selected time-windows
    for f in range(0,len(fldr)):
        print('--' + fldr[f])
        pres = []
        num = []
        path = cnpt + '//' + fldr[f] + '//Predictions//'
        for i in range(1, len(os.listdir(path)) + 1):
            neg = 0
            tt = 0
            tf = 0
            num.append(i)
            #the database (in a csv file) is opened and stored in 'base'
            r = open(path + '//Prediction' + str(i) + '.csv','r')
            r_txt = r.read()
            r.close()
            base = r_txt.split('\n')
            y_exp = []
            y_prd = []
            for j in range(1,len(base)):
                ln = str(base[j])
                q = ln.split(',')
                if(len(q) > 1)and((q[0]!='')and(q[0]!=' ')):
                    y_prd.append(float(q[-2]))
                    y_exp.append(float(q[-1]))
            #accuracy
            acc = 100*met.accuracy_score(y_exp,y_prd)
            #precision
            ppv = 100*met.precision_score(y_exp,y_prd)
            #f1 score
            fsc = 100*met.f1_score(y_exp,y_prd)
            #recall
            rec = 100*met.recall_score(y_exp,y_prd)
            pres.append([acc,ppv,rec,fsc])
        #A csv file with the scores is written
        w = open(cnpt + '//' + fldr[f] + '//PreSelectionReport_' + fldr[f] + '_' + cnpt + '.csv', 'w')
        try:
            w.write('Accuracy')
            temp = []
            for arr in pres:
                w.write(',' + str(arr[0]))
                temp.append(arr[0])
            w.write('\n')
            mu = np.mean(temp)
            w.write('Avg. Accuracy,' + str(mu) + '\n')
            w.write('Precision')
            temp = []
            for arr in pres:
                w.write(',' + str(arr[1]))
                temp.append(arr[1])
            w.write('\n')
            mu = np.mean(temp)
            w.write('Avg. Precision,' + str(mu) + '\n')
            w.write('Recall')
            temp = []
            for arr in pres:
                w.write(',' + str(arr[2]))
                temp.append(arr[2])
            w.write('\n')
            mu = np.mean(temp)
            w.write('Avg. Recall,' + str(mu) + '\n')
            w.write('F1Score')
            temp = []
            for arr in pres:
                w.write(',' + str(arr[3]))
                temp.append(arr[3])
            w.write('\n')
            mu = np.mean(temp)
            w.write('Avg. F1Score,' + str(mu))
        except Exception as e:
            print('-----An error ocurred: ' + str(e))
        w.close()
        print('---' + fldr[f] + ' done')    
print('End of program')
