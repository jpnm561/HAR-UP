# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 11:48:03 2018

@author: José Pablo
"""

from sklearn.ensemble import RandomForestClassifier as RndFC
from sklearn import svm
from sklearn import metrics as met
from sklearn.neural_network import MLPClassifier as ffp
from sklearn.neighbors import KNeighborsClassifier as KNN
import numpy as np
import random as rnd
from createFolder import createFolder
import matplotlib.pyplot as plt
from scorePlots import plotScore, plot_confusion_matrix

"""
 -----------------------------------------------------------------------------------------------------
 Functions
 ----------------------------------------------------------------------------------------------------- 
 """
def cleanLine(line, header = False):
    line = line.replace("'",'')
    line = line.replace("[",'')
    line = line.replace("]",'')
    if header:
        line = line.replace('\ ','')
    else:
        line = line.replace("?",'NaN')
    arr = line.split(',')
    return arr

def MC_Training(concept,
            t_window=['1&0.5','2&1','3&1.5'],
            methods = ['RF','SVM','MLP','KNN']):
    for cncpt in concept:
        for twnd in t_window:
            d_base = []
            f_dbase = 'SelectedFeatures_'+twnd+'_'+cncpt+'.csv'
            r = open(cncpt + '//' + twnd + '//' + f_dbase,'r')
            txt = r.read()
            r.close()
            d_base = txt.split('\n')
            
            #an array to store the features (columns in the csv, without the tag)
            features = []
            feat = cleanLine(d_base[0],True)
            for i in range(0, len(feat) - 1):
                features.append(feat[i])
            
            for k in range(0, 10):
                #70% of the data base is randomly selected
                n_tr = int((len(d_base)*0.7)//1)
                r_arr = []
                for l in range(0, n_tr): 
                    while(True):
                        n_rnd = rnd.randint(1, len(d_base) - 1)
                        if len(r_arr) == 0:
                            r_arr.append(n_rnd)
                            break
                        else:
                            flg = True
                            for num in r_arr:
                                if num == n_rnd:
                                    flg = False
                                    break
                            if flg == True:
                                r_arr.append(n_rnd)
                                break
                #input (x) and output (y) arrays for training
                x_tr = []
                y_tr = []
                #input (x) and output (y) arrays for validation
                x_30 = []
                y_30 = []
                #To know if something should be ignored
                ignr = -1
                for i in range(1,len(d_base)):
                    ln = str(d_base[i])
                    q = cleanLine(ln)
                    if (q[0]!=' ')and(q[0]!=''):
                        p = []
                        for j in range(0, len(features)):
                            if(j < len(q)-1):
                                p.append(float(q[j]))
                        flg = False
                        for num in r_arr:
                            if num == i:
                                flg = True
                                break
                        if flg == True:
                            y_tr.append(float(q[len(features)]))
                            x_tr.append(p)
                        else:
                            y_30.append(float(q[len(features)]))
                            x_30.append(p)
                    else:
                        if (i + 1) == len(d_base):
                            ignr = i
                        else:
                            print('There is an empty line!!!\n \tLine: '+str(i+1)+' / '+str(len(d_base)))
                X = np.array([np.array(z) for z in x_tr])
                for method in methods:
                    if method == 'RF':
                        clsf = RndFC(n_estimators=10)
                    elif method == 'SVM':
                        clsf = svm.SVC(gamma='auto')
                    elif method == 'MLP': 
                        clsf = ffp()
                    else:
                        clsf = KNN()
                    clsf.fit(X,y_tr)
                    Xr = np.array([np.array(z) for z in x_30])
                    Y = clsf.predict(Xr)    
                    st = ""
                    for i in range(0, len(features)):
                        st += features[i] +','
                    st += 'Output,Expected' + '\n'
                    path = cncpt+'//'+twnd+'//'+method
                    createFolder(path)
                    doc = path+'//Result_'+twnd+'_'+method+'_'+str(k+1)+'.csv'
                    w = open(doc, 'w')
                    print('-----Writing...')
                    try:
                        w.write(st)
                        a = 0
                        for i in range(1, len(d_base)):
                            if i!= ignr:
                                flg = True
                                for nmb in r_arr:
                                    if nmb == i:
                                        flg = False
                                        break
                                if flg == True:
                                    q = d_base[i].split(',')
                                    for j in range(0, len(features)):
                                        w.write(q[j] + ',')
                                    w.write(str(Y[a]) + ',' + str(y_30[a]) + '\n')
                                    a += 1
                    except Exception as e:
                        print('----Unexpected error: ' + str(e))
                    w.close()
                    print('-----' + str(a) + '/' + str(len(d_base)-1))
                    print('----...Prediction ' + str(k+1) + ' ' + method + ' finished')

     
def write_score(w, score, arr,ln_flg = False):
    w.write(score + '\n')
    for i in range(0, len(arr)):
        w.write(str(arr[i]))
        if i < len(arr) - 1:
            w.write(',')
    w.write('\n')
    #mean
    mu = np.mean(arr)
    #standard deviation
    sig = np.std(arr)
    w.write('Mean,' + str(mu) + '\n')
    w.write('SD,' + str(sig))
    if ln_flg:
        w.write('\n')
    return [mu,sig]

def writeFinal(w, score, arr, t_window, methods, ln_flg = False):
    w.write(score + '\n')
    for method in methods:
        w.write(',' + method +',')
    for i in range(0,len(t_window)):
        w.write('\n' + t_window[i])
        for j in range(0,len(methods)):
            for k in range(0,2):
                w.write(','+str(arr[i][j][k]))
    if ln_flg:
        w.write('\n')
 
def MC_Scores(concept,
            t_window=['1&0.5','2&1','3&1.5'],
            methods = ['RF','SVM','MLP','KNN']):            
    for cncpt in concept:
        print(cncpt)
        acc_e = []
        ppv_e = []
        fsc_e = []
        rec_e = []
        cmat_e = []
        for twnd in t_window:
            print('--' + twnd)
            acc_arr = []
            ppv_arr = []
            fsc_arr = []
            rec_arr = []
            cmat_arr = []
            for method in methods:
                acc_prom = []
                ppv_prom = []
                fsc_prom = []
                rec_prom = []
                cmat_prom = []
                for i in range(1,11):
                    tp = 0
                    tn = 0
                    pos = 0
                    neg = 0
                    y_true = []
                    y_pred = []
                    doc = cncpt+'//'+twnd+'//'+method+'//Result_'+twnd+'_'+method+'_'+str(i)+'.csv'
                    r = open(doc,'r')
                    txt = r.read()
                    r.close()
                    d_base = txt.split('\n')
                    for j in range(1,len(d_base)):
                        ln = str(d_base[j])
                        q = ln.split(',')
                        if(len(q) > 1):
                            pred = float(q[len(q)-2])
                            y_pred.append(pred)
                            yesp = float(q[len(q)-1])
                            y_true.append(yesp)
                            bnd = True
                            if yesp == 0:
                                neg += 1
                            else:
                                pos += 1
                                bnd = False
                            if(pred == yesp):
                                if bnd:
                                    tn += 1
                                else:
                                    tp += 1
                    if(pos == 0):
                        print('No falls in: ' + cncpt + '-' + twnd + '-' + str(j + 1))
                    
                    acc = 100*met.accuracy_score(y_true,y_pred)
                    ppv = 100*met.precision_score(y_true,y_pred,average='macro')
                    fsc = 100*met.f1_score(y_true,y_pred,average='macro')
                    rec = 100*met.recall_score(y_true,y_pred,average='macro')
                    
                    acc_prom.append(acc)
                    ppv_prom.append(ppv)
                    fsc_prom.append(fsc)
                    rec_prom.append(rec)
                    
                    c_mat = met.confusion_matrix(y_true,y_pred)
                    c_mat = c_mat.astype('float') / c_mat.sum(axis=1)[:,np.newaxis]
                    cmat_prom.append(c_mat)
                    
                odoc = cncpt+'//'+twnd+'//Score_'+twnd+'_'+method+'.csv'
                w = open(odoc, 'w')
                try:
                    acc_arr.append(write_score(w,'Accuracy',acc_prom,True))
                    ppv_arr.append(write_score(w,'Precision',ppv_prom,True))
                    rec_arr.append(write_score(w,'Recall',rec_prom,True))
                    fsc_arr.append(write_score(w,'F1Score',fsc_prom))
                    print('----' + method + ' ' + twnd + ' done')
                except Exception as e:
                    print('----ERROR: ' + str(e))
                w.close()
                
                #Graphs
                temp_arr = []
                for e_y in range(0,12):
                    tmp_ln = []
                    for e_x in range(0,12):
                        tmp_var = 0
                        for mat in range(0,len(cmat_prom)):
                            tmp_var += cmat_prom[mat][e_y][e_x]
                        tmp_var = tmp_var/len(cmat_prom)
                        tmp_ln.append(tmp_var)
                    temp_arr.append(tmp_ln)
                cmat_arr.append(temp_arr)
                title = 'Avg. Confusion Matrix '+twnd+' '+method+' '+cncpt
                title_save = 'AvgConfusionMatrix_'+twnd+'_'+method+'_'+cncpt
                classes = ['1','2','3','4','5','6','7','8','9','10','11','20']
                cf_mat = np.array(temp_arr) 
                np.set_printoptions(precision=2)
                plt.figure()
                plot_confusion_matrix(cf_mat,classes = classes,normalize=True,title=title)
                plt.savefig(cncpt+'//'+twnd+'//'+title_save+'.jpg',dpi=100)
                plt.close()
            acc_e.append(acc_arr)
            ppv_e.append(ppv_arr)
            rec_e.append(rec_arr)
            fsc_e.append(fsc_arr)
            cmat_e.append(cmat_arr)
        w = open(cncpt + '//Score_' + cncpt +'_temp.csv','w')
        try:
            writeFinal(w,'Accuracy',acc_e,t_window,methods,True)
            writeFinal(w,'Precision',ppv_e,t_window,methods,True)
            writeFinal(w,'Recall',rec_e,t_window,methods,True)
            writeFinal(w,'F1Score',fsc_e,t_window,methods)
        except Exception as e:
            print(e)
        w.close()
        #plotting the scores
        plotScore([acc_e,ppv_e,rec_e,fsc_e],cncpt,t_window=t_window,methods=methods)
        #Average confusion matrix
        for mthd in range(0,len(methods)):
            temp_arr = []
            method = methods[mthd]
            print('----'+methods[mthd])
            for e_y in range(0,12):
                tmp_ln = []
                for e_x in range(0,12):
                    tmp_var = 0
                    for tw in range(0,len(t_window)):
                        tmp_var += cmat_e[tw][mthd][e_y][e_x]
                    tmp_var = tmp_var/len(t_window)
                    tmp_ln.append(tmp_var)
                temp_arr.append(tmp_ln)
            title = 'Avg. Confusion Matrix ' + method+ ' ' + cncpt
            classes = ['1','2','3','4','5','6','7','8','9','10','11','20']
            cf_mat = np.array(temp_arr)
            np.set_printoptions(precision=2)
            plt.figure()
            plot_confusion_matrix(cf_mat,classes = classes,normalize=True,title=title)
            plt.savefig(cncpt+'//AvgConfusionMatrix_'+method+'_'+cncpt+'.jpg',dpi=100)
            plt.close()

"""
 -----------------------------------------------------------------------------------------------------
 End of functions
 ----------------------------------------------------------------------------------------------------- 
"""
def main():
    concept = []
    MC_Training(concept)
    MC_Scores(concept)

if __name__ == "__main__":
    main()
