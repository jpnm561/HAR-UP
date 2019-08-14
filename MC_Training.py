# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 11:48:03 2018

@author: José Pablo
"""

from sklearn.ensemble import RandomForestClassifier as RndFC
from sklearn import svm
from sklearn.neural_network import MLPClassifier as ffp
from sklearn.neighbors import KNeighborsClassifier as KNN
import numpy as np
import csv
import random as rnd


#The different time windows for our experiments
fldrs = ['1&0.5', '2&1', '3&1.5']
fbase = 'TrainFts.csv'
cncpt = 'IMU_Head'
#sect = "---------------------------------------------------------------------\n"
sect = ""
for spr in range(0, 3):
    base = []
    features = []
    
    r = open(cncpt + '//' + fldrs[spr] + '//' + fbase,'r')
    txt = r.read()
    r.close
    base = txt.split('\n')
    
    temp = str(base[0])
    temp = temp.replace("'",'')
    temp = temp.replace('\ ','')
    feat = temp.split(',')
    for i in range(0, len(feat) - 1):
        features.append(feat[i])
    
    #for k in range(len(features)-2, len(features)):
    for k in range(0, 10):
        #70% of the data base is selected for training
        ttr = int((len(base)*0.7)//1)
        rarr = []
        for l in range(0, ttr): 
            while(True):
                #We add random lines to our array for training
                nal = rnd.randint(1, len(base) - 1)
                if len(rarr) == 0:
                    rarr.append(nal)
                    break
                else:
                    flg = True
                    for num in rarr:
                        if num == nal:
                            flg = False
                            break
                    if flg == True:
                        rarr.append(nal)
                        break
        x_tr = []
        y_tr = []
        x_30 = []
        y_30 = []
        for i in range(1,len(base)):
            ln = str(base[i])
            ln = ln.replace("'",'')
            ln = ln.replace("[",'')
            ln = ln.replace("]",'')
            ln = ln.replace("?",'NaN')
            q = ln.split(',')
            p = []
            for j in range(0, len(features)):
                if(j < len(q)-1):
                    p.append(float(q[j]))
            flg = False
            for nmb in rarr:
                if nmb == i:
                    flg = True
                    break
            if flg == True:
                y_tr.append(float(q[len(features)]))
                x_tr.append(p)
            else:
                y_30.append(float(q[len(features)]))
                x_30.append(p)                
        X = np.array([np.array(z) for z in x_tr])
        for fi in range (0,4):
            typ = ''
            if fi == 0:
                clsf = RndFC()
                typ = 'RF_'
            elif fi == 1:
                clsf = svm.SVC()
                typ = 'SVM_'
            elif fi == 2: 
                clsf = ffp()
                typ = 'RN_'
            else:
                clsf = KNN()
                typ = 'KNN_'
            clsf.fit(X,y_tr)
            Xr = np.array([np.array(z) for z in x_30])
            Y = clsf.predict(Xr)    
            st = ""
            for i in range(0, len(features)):
                st += features[i] +','
            st += 'Predicted,Expected' + '\n'
            doc = cncpt+'//'+fldrs[spr]+'//Result_'+fldrs[spr]+'_'+typ+str(k+1)+'.csv'
            w = open(doc, 'w')
            w.write(st)
            srt = ""
            a = 0
            for i in range(1, len(base)):
                flg = True
                for nmb in rarr:
                    if nmb == i:
                        flg = False
                        break
                if flg == True:
                    ln = str(base[i])
                    ln = ln.replace("'",'')
                    ln = ln.replace("[",'')
                    ln = ln.replace("]",'')
                    ln = ln.replace("?",'NaN')
                    q = ln.split(',')
                    for j in range(0, len(features)):
                        w.write(q[j] + ',')
                    w.write(str(Y[a]) + ',' + str(y_30[a]) + '\n')
                    a += 1
            w.close()
            print(a)
            print('Prediction ' + str(k+1) + ' ' + typ + 'is done')
print('End of program')
