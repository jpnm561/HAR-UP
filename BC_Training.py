# -*- coding: utf-8 -*-
"""
Created on Tue Feb 19 00:42:57 2019

@author: José Pablo
"""

from sklearn.ensemble import RandomForestClassifier as RndFC
from sklearn import svm
from sklearn.neural_network import MLPClassifier as ffp
from sklearn.neighbors import KNeighborsClassifier as KNN
import numpy as np
import random as rnd
import os


def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)

fldrs = ['1&0.5', '2&1', '3&1.5']

concept = ['IMU','IR_Vision']

for cncpt in concept:
    print(cncpt)
    for f in range(0, len(fldrs):
        base = []
        #a flag to check that the database has no empty rows
        mflg = True
        fbase = 'SelectedFeatures_'+fldrs[f]+'_'+cncpt+'.csv'
        r = open(cncpt + '//' + fldrs[f] + '//' + fbase,'r')
        txt = r.read()
        r.close
        base = txt.split('\n')
        
        #an array to store the features (columns in the csv, without the tag)
        features = []
        feat = base[0].split(',')
        for i in range(0, len(feat) - 1):
            features.append(feat[i])
        
        #an array to save every fall index (falls are tagged with '1')
        falls = []
        #an array to save every non-fall index (tagged with '0')
        other = []
        #to ignore an empty row at the end of the file (if there is one)
        ignr = -1
        
        for i in range(1,len(base)):
            ln = base[i].split(',')
            #we check that we don't have an empty row and we make arrays to save the indexes for falls and the other activities
            if (ln[0]!=' ')and(ln[0]!=''):
                if int(ln[-1]) == 0:
                    other.append(i)
                else:
                    falls.append(i)
            else:
                if (i+1)==len(base):
                    ignr = i
                else:
                    #should an empty row that is not at the end exist
                    print('There is an empty row!!! ' + str(i+1)+'/'+str(len(base)))
                    print('*** ' + base[i])
                    mflg = False
        if mflg:
            print('----Falls = ' + str(len(falls)) + ' ; Other = ' + str(len(other)))
            #Training is performed with 70% of the database, the other 30% is used for validation
            ntr_falls = int((len(falls)*0.7)//1)
            ntr_other = int((len(other)*0.7)//1)
            print('----Training_Falls = ' + str(ntr_falls) + ' ; Training_Other = ' + str(ntr_other))
            #Training and validation is performed 10 times for each model, with data for training selected randomly
            for k in range(0, 10):
                #an array with the selected indexes for training (within 'falls')
                rarr_f = []
                for l in range(0,ntr_falls): 
                    while(True):
                        n_rnd = rnd.randint(0, len(falls) - 1)
                        if len(rarr_f) == 0:
                            rarr_f.append(n_rnd)
                            break
                        else:
                            flg = True
                            for num in rarr_f:
                                if num == n_rnd:
                                    flg = False
                                    break
                            if flg:
                                rarr_f.append(n_rnd)
                                break                   
                #an array with the selected indexes for training (within 'other')
                rarr_o = []
                for l in range(0,ntr_other): 
                    while(True):
                        n_rnd = rnd.randint(0, len(other) - 1)
                        if len(rarr_o) == 0:
                            rarr_o.append(n_rnd)
                            break
                        else:
                            flg = True
                            for num in rarr_o:
                                if num == n_rnd:
                                    flg = False
                                    break
                            if flg:
                                rarr_o.append(n_rnd)
                                break
                #we make the array with the fall indexes (from 'base') that will be used for training
                tr_falls = []
                for l in rarr_f:
                    tr_falls.append(falls[l])
                #we make the array with the other activiies indexes (from 'base') that will be used for training
                tr_other = []
                for l in rarr_o:
                    tr_other.append(other[l])            
                #input (x) and output (y) arrays for training
                x_tr = []
                y_tr = []
                #input (x) and output (y) arrays for validation
                x_30 = []
                y_30 = []
                for i in range(1,len(base)):
                    #we check that we are not dealing with an empty row (at the end)
                    if i != ignr:
                        #an arbitrary array with all the elements of a row
                        q = base[i].split(',')
                        #an arbitrary array to contain all the inputs (features) in a row
                        p = []
                        for j in range(0, len(q) - 1):
                            p.append(float(q[j]))
                        #We check if is one of the rows used for training to fill the input and output arrays
                        flg = False
                        for nmb in tr_falls:
                            if nmb == i:
                                flg = True
                                break
                        if flg:
                            y_tr.append(float(q[-1]))
                            x_tr.append(p)
                        else:
                            for nmb in tr_other:
                                if nmb == i:
                                    flg = True
                                    break
                            if flg:
                                y_tr.append(float(q[-1]))
                                x_tr.append(p)
                            else:
                                y_30.append(float(q[-1]))
                                x_30.append(p)                
                #we make a numpy array for training
                X = np.array([np.array(z) for z in x_tr])
                #this is done for each one of the 4 methods
                for fi in range (0,4):
                    typ = ''
                    #random forest
                    if fi == 0:
                        clsf = RndFC()
                        typ = 'RF'
                    #support vecctor machines
                    elif fi == 1:
                        clsf = svm.SVC()
                        typ = 'SVM'
                    #multi-layer perceptron networks
                    elif fi == 2: 
                        clsf = ffp()
                        typ = 'MLP'
                    #k-nearest neighbour
                    else:
                        clsf = KNN()
                        typ = 'KNN'
                    #training is performed
                    clsf.fit(X,y_tr)
                    #a numpy array is made for validation
                    Xr = np.array([np.array(z) for z in x_30])
                    #the output (for validation) is obtained
                    Y = clsf.predict(Xr)
                    #an arbitrary string variable to write a csv file
                    st = ''
                    for i in range(0, len(features)):
                        st += features[i] +','
                    st += 'Predicted,Expected' + '\n'
                    path = cncpt+'//'+fldrs[f]+'//'+typ
                    createFolder(path)
                    doc = path+'//Result_'+fldrs[f]+'_'+typ+'_'+str(k+1)+'.csv'
                    print('----Writing...')
                    #we make a csv file with the data for validation, the predicted output and the expected (real) output
                    w = open(doc, 'w')
                    try:
                        w.write(st)
                        srt = ""
                        a = 0
                        for i in range(1, len(base)):
                            if ignr != i:
                                flg = True
                                for nmb in tr_falls:
                                    if nmb == i:
                                        flg = False
                                        break
                                if flg:
                                    for nmb in tr_other:
                                        if nmb == i:
                                            flg = False
                                            break
                                if flg:
                                    q = base[i].split(',')
                                    for j in range(0, len(features)):
                                        w.write(q[j] + ',')
                                    w.write(str(Y[a]) + ',' + str(y_30[a]) + '\n')
                                    a += 1
                    except Exception as e:
                        print(str(f)+'::'+str(k)+':  '+str(e))
                    w.close()
                    print('-----' + str(a) + '/' + str(len(base)-1))
                    print('----...Prediction ' + str(k+1) + ' ' + typ + ' finished')
print('End of program')
