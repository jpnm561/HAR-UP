# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 19:43:36 2019

@author: 0169723
"""

import numpy as np
from progressBar import progressBar
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.feature_selection import SelectFromModel
from sklearn.svm import LinearSVC
import pandas as pd
from PreSelector import preSelector

"""
-------------------------------------------------------------------------------
Functions
-------------------------------------------------------------------------------
"""


#ExtraTree decision forest for Feature Selection
def treeClss(X,y):
    forest = ExtraTreesClassifier(n_estimators=250,
                                  random_state=0)
    forest.fit(X, y)
    importances = forest.feature_importances_
    indices = np.argsort(importances)[::-1]
    selection = []
    for f in range(X.shape[1]):
        if f < 100:
            selection.append(indices[f])
        else:
            break
    return selection

#L2 classification with linear SVC for Feature Selection
def l2SM(X,y):
    lsvc = LinearSVC(C=1.00, penalty="l2", dual=False).fit(X, y)
    model = SelectFromModel(lsvc, prefit=True)
    X_new = model.transform(X)
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
    
def freq(path,arr_1,arr_2,features):
    i_flg = False
    arr = []
    f_arr = join([], arr_1)
    f_arr = join(f_arr, arr_2)
    w =  open(path, 'w')
    try:
        w.write('Attribute No,Attribute,Frequency')
        for f in f_arr:
            i = 0
            i = quantity(arr_1, f, i)
            i = quantity(arr_2, f, i)
            w.write('\n' + str(f+1) + ',' + features[f] + ',' + str(i))
            arr.append([f,i])
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

"""
-------------------------------------------------------------------------------
End of functions
-------------------------------------------------------------------------------
"""

def main():
    db_path = 'IMU_Head_IR_1&0.5.csv'
    df = pd.read_csv(db_path)
    df.head()
    df.columns[-1]
    X = df[df.columns[0:-1]].values
    y = df[' Tag'].values  #'Tag'
    print('Data sorted')  
    features = []
    for i in range(0,len(df.columns)-1):
        features.append(df.columns[i])
    print('Features reached')    
    
    a = treeClss(X,y)
    b = l2SM(X,y)
    
    arr = freq('PreSelection.csv',a,b,features)
    if type(arr) != bool:
        print(arr)
    
if __name__=="__main__":
    main()
