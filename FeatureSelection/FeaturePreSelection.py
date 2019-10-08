# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 19:43:36 2019

@author: 0169723
"""

import numpy as np
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.feature_selection import SelectFromModel, RFE
from sklearn.ensemble import RandomForestClassifier as RndFC
from sklearn.svm import LinearSVC
import pandas as pd
from createFolder import createFolder
from progressBar import progressBar

"""
-------------------------------------------------------------------------------
Functions
-------------------------------------------------------------------------------
"""


#ExtraTree decision forest for Feature Selection
def treeClss(X,y):
    q = 99
    if X.shape[1] < 100:
        q = X.shape[1]
    progressBar('----Extra trees',0,q)
    forest = ExtraTreesClassifier(n_estimators=250,
                                  random_state=0)
    forest.fit(X, y)
    importances = forest.feature_importances_
    indices = np.argsort(importances)[::-1]
    selection = []
    for f in range(X.shape[1]):
        if f < 100:
            selection.append(indices[f])
            progressBar('----Extra trees',f,q)
        else:
            break
    return selection

#L2 classification with linear SVC for Feature Selection
def l2SM(X,y):
    q = 100
    progressBar('----Linear SVC ',0,q)
    lsvc = LinearSVC(C=1.00, penalty="l2", dual=False).fit(X, y)
    model = SelectFromModel(lsvc, prefit=True)
    X_new = model.transform(X)
    if X_new.shape[1] < 100:
        q = X_new.shape[1]
    p = 0
    selection = []
    for f in range(X_new.shape[1]):
        for i in range(X.shape[1]):
            flg = True
            for j in range(X.shape[0]):
                if X[j][i] != X_new[j][f]:
                    flg = False
                    break
            if flg and (len(selection)<=100):
                selection.append(i)
                p += 1
                progressBar('----Linear SVC ',p,q)
    return selection

#Recursive Feature elimination with Random Forest
def rfRFE(X,y):
    q = 100
    if X.shape[1] < 100:
        q = int(X.shape[1]*0.3)
    progressBar('----RFE with RF',0,int(q*1.3))
    estimator = RndFC(n_estimators = 10)
    selector = RFE(estimator, q, step=1)
    progressBar('----RFE with RF',int(q*0.2),int(q*1.3))
    selector = selector.fit(X, y)
    progressBar('----RFE with RF',q,int(q*1.3))
    selection = selector.get_support(1)
    progressBar('----RFE with RF',int(q*1.3),int(q*1.3))
    return selection

def join(f_arr,s_arr):
    for i in range(0,len(s_arr)):
        bnd = True
        for f in f_arr:
            if s_arr[i] == f:
                bnd = False
                break
        if bnd:
            f_arr.append(s_arr[i])
    return f_arr

def quantity(s_arr, f, i):
    for n in s_arr:
        if n == f:
            i+=1
            break
    return i
    
def freq(path,arr_1,arr_2,arr_3,features):
    i_flg = False
    arr = []
    f_arr = join([], arr_1)
    f_arr = join(f_arr, arr_2)
    f_arr = join(f_arr, arr_3)
    w =  open(path, 'w')
    p = 0
    q = len(f_arr)
    try:
        progressBar('----Frequencies',p,q)
        w.write('Attribute No,Attribute,Frequency')
        for f in f_arr:
            i = 0
            i = quantity(arr_1, f, i)
            i = quantity(arr_2, f, i)
            i = quantity(arr_3, f, i)
            w.write('\n' + str(f+1) + ',' + features[f] + ',' + str(i))
            arr.append([f,i])
            p += 1
            progressBar('----Frequencies',p,q)
    except KeyboardInterrupt:
        print('The program has been aborted by the user')
        i_flg = True
    except Exception as e:
        print('Unexpected error: ' + str(e))
    w.close()
    if not i_flg:
        temp = []
        for i in range(0,len(f_arr)):
            for j in range(i,len(f_arr)):
                if arr[i][1] < arr[j][1]:
                    temp = arr[i]
                    arr[i] = arr[j]
                    arr[j] = temp
        s_arr = []
        for i in range(0,len(f_arr)):
            if arr[i][1] > 1:
                s_arr.append(arr[i][0])
        s_arr.append(0)
        return s_arr    
    return i_flg    

def writeDocument(cncpt,
                  features,
                  X,
                  y,
                  s_arr,
                  twnd):
    path = cncpt+'//'+twnd+'//'
    createFolder(path)
    p = 0
    q = len(s_arr) + X.shape[0]
    w = open(path + 'PreSelectedFTS_'+twnd+'_'+cncpt+'.csv', 'w')
    try:
        for i in range(0, len(s_arr)):
            w.write(str(features[s_arr[i]]) + ',')
            p += 1
            progressBar('----Output file',p,q)
        w.write('Tag\n')
        for i in range(0, X.shape[0]):
            for j in range(0, len(s_arr)):
                w.write(str(X[i][s_arr[j]]) + ',')
            w.write(str(y[i]))
            if i < X.shape[0]-1:
                w.write('\n')
            p += 1
            progressBar('----Output file',p,q)
    except KeyboardInterrupt:
        print('The program has been interrupted by the user.')
    except Exception as e:
        print('Unexpected error: ' + str(e))
    w.close()

def preSelection(concept,
                 t_window=['1&0.5','2&1','3&1.5'],
                 path = ''):
    for cncpt in concept:
        print(cncpt)
        for twnd in t_window:
            print('--%s' %(twnd))
            df = pd.read_csv(path + cncpt + '//' + twnd + '//' + cncpt + '_' + twnd + '.csv')
            df.head()
            df.columns[-1]
            X = df[df.columns[0:-1]].values
            error = False
            try:
                y = df[' Tag'].values
            except Exception as e:
                if str(e) == 'Tag':
                    y = df[' Tag'].values  #'Tag'
                else:
                    error = True
                    print('Unexpected error: ' + str(e))
            if not error:
                print('----Data sorted')
                features = []
                for i in range(0,len(df.columns)-1):
                    features.append(df.columns[i])
            
                arr1 = treeClss(X,y)
                arr2 = rfRFE(X,y)
                arr3 = l2SM(X,y)
                
                arr = freq(cncpt+'//'+twnd+'//PreSelection.csv',arr1,arr2,arr3,features)
                if type(arr) != bool:
                    writeDocument(cncpt,features,X,y,arr,twnd)

                    
"""
-------------------------------------------------------------------------------
End of functions
-------------------------------------------------------------------------------
"""

def main():
    concept = []
    preSelection(concept)
    print('End of task')
    
if __name__=="__main__":
    main()
