# -*- coding: utf-8 -*-
"""
Created on Tue Feb 19 00:42:57 2019

@author: José Pablo
"""

from sklearn.ensemble import RandomForestClassifier as RndFC
from sklearn import svm
from sklearn import metrics as met
from sklearn.neural_network import MLPClassifier as ffp
from sklearn.neighbors import KNeighborsClassifier as KNN
from createFolder import createFolder
import numpy as np
import random as rnd
import os
import matplotlib.pyplot as plt
from scorePlots import plotScore, plot_confusion_matrix

def BC_Training(concept,
            t_window=['1&0.5','2&1','3&1.5'],
            methods = ['RF','SVM','MLP','KNN']):
    for cncpt in concept:
        print(cncpt)
        for twnd in t_window:
            d_base = []
            #a flag to check that the database has no empty rows
            mflg = True
            f_dbase = 'SelectedFeatures_'+twnd+'_'+cncpt+'.csv'
            r = open(cncpt + '//' + twnd + '//' + f_dbase,'r')
            txt = r.read()
            r.close
            d_base = txt.split('\n')
            
            #an array to store the features (columns in the csv, without the tag)
            features = []
            feat = d_base[0].split(',')
            for i in range(0, len(feat) - 1):
                features.append(feat[i])
            
            #an array to save every fall index (falls are tagged with '1')
            falls = []
            #an array to save every non-fall index (tagged with '0')
            other = []
            #to ignore an empty row at the end of the file (if there is one)
            ignr = -1
            
            for i in range(1,len(d_base)):
                ln = d_base[i].split(',')
                #we check that we don't have an empty row and we make arrays to save the indexes for falls and the other activities
                if (ln[0]!=' ')and(ln[0]!=''):
                    if int(ln[-1]) == 0:
                        other.append(i)
                    else:
                        falls.append(i)
                else:
                    if (i+1)==len(d_base):
                        ignr = i
                    else:
                        #should an empty row that is not at the end exist
                        print('There is an empty row!!! ' + str(i+1)+'/'+str(len(d_base)))
                        print('*** ' + d_base[i])
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
                    for i in range(1,len(d_base)):
                        #we check that we are not dealing with an empty row (at the end)
                        if i != ignr:
                            #an arbitrary array with all the elements of a row
                            q = d_base[i].split(',')
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
                    for method in methods:
                        #random forest
                        if method == 'RF':
                            clsf = RndFC(n_estimators=10)
                        #support vecctor machines
                        elif method == 'SVM':
                            clsf = svm.SVC(gamma='auto')
                        #multi-layer perceptron networks
                        elif method == 'MLP': 
                            clsf = ffp()
                        #k-nearest neighbour
                        else:
                            clsf = KNN()
                        
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
                        st += 'Output,Expected' + '\n'
                        path = cncpt+'//'+twnd+'//'+method
                        createFolder(path)
                        doc = path+'//Result_'+twnd+'_'+method+'_'+str(k+1)+'.csv'
                        print('----Writing...')
                        #we make a csv file with the data for validation, the predicted output and the expected (real) output
                        w = open(doc, 'w')
                        try:
                            w.write(st)
                            srt = ""
                            a = 0
                            for i in range(1, len(d_base)):
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
    w.write('DS,' + str(sig))
    if ln_flg:
        w.write('\n')
    return [mu,sig]

def writeFinal(w, score, arr, t_window, methods, ln_flg = False):
    w.write(socre + '\n')
    for method in methods:
        w.write(',' + method +',')
    for i in range(0,len(t_window)):
        w.write('\n' + t_window[i])
        for j in range(0,len(methods)):
            for k in range(0,2):
                w.write(','+str(arr[i][j][k]))
    if ln_flg:
        w.write('\n')

def BC_Scores(concept,
            t_window=['1&0.5','2&1','3&1.5'],
            methods = ['RF','SVM','MLP','KNN']):
    for cncpt in concept:
        print(cncpt)
        #an array to save the accuracy for every method, with each time-window
        acc_e = []
        #an array to save the precison for every method, with each time-window
        ppv_e = []
        #an array to save the f1-score for every method, with each time-window
        fsc_e = []
        #an array to save the recall for every method, with each time-window
        rec_e = []
        #an array to save the true positives for every method, with each time-window
        tpn_e = []
        #an array to save the true negatives for every method, with each time-window
        tnn_e = []
        for twnd in t_window:  #time window
            print('--' + twnd)
            acc_arr = []
            ppv_arr = []
            fsc_arr = []
            rec_arr = []
            tpn_arr = []
            tnn_arr = []
            for method in methods:  #method
                #arrays with the scores for the 10 results, an average will be made with these values
                acc_avg = []
                ppv_avg = []
                fsc_avg = []
                rec_avg = []
                tpn_avg = []
                tnn_avg = []
                #for the ten results
                for i in range(1,11):
                    tp = 0   #true positive outputs
                    tn = 0   #true negative outputs
                    pos = 0  #positive outputs
                    neg = 0  #negative outputs
                    #an array for the expected (true) output values
                    y_true = []
                    #an array for the predicted output values
                    y_pred = []
                    doc = cncpt+'//'+twnd+'//'+method+'//Resultado_'+twnd+'_'+method+'_'+str(i)+'.csv'
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
                            yexp = float(q[len(q)-1])
                            y_true.append(yexp)
                            bnd = True
                            if yexp == 0:
                                neg += 1
                            else:
                                pos += 1
                                flg = False
                            if(pred == yexp):
                                if flg:
                                    tn += 1
                                else:
                                    tp += 1
                    #To notify if there were no falls in the sample
                    if(pos == 0):
                        print('There were no falls in: ' + cncpt + '-' + twnd + '-' + str(j + 1))
                    #Scores are calculated (as a percentage)
                    acc = 100*met.accuracy_score(y_true,y_pred)
                    ppv = 100*met.precision_score(y_true,y_pred)
                    fsc = 100*met.f1_score(y_true,y_pred)
                    rec = 100*met.recall_score(y_true,y_pred)
                    
                    acc_avg.append(acc)
                    ppv_avg.append(ppv)
                    fsc_avg.append(fsc)
                    rec_avg.append(rec)
                    tpn_avg.append(tp/pos)
                    tnn_avg.append(tn/neg)
                    
                odoc = cncpt+'//'+twnd+'//Score_'+twnd+'_'+method+'.csv'
                w = open(odoc, 'w')
                try:
                    acc_arr.append(write_score(w,'Accuracy',acc_avg,True))
                    ppv_arr.append(write_score(w,'Precision',ppv_avg,True))
                    rec_arr.append(write_score(w,'Recall',rec_avg,True))
                    fsc_arr.append(write_score(w,'F1Score',fsc_avg))
                    print('----' + method + ' ' + twnd + ' done')
                except Exception as e:
                    print('----ERROR: ' + str(e))
                w.close()
                #Plotting the confusion matrix
                tp_mu = np.mean(tpn_avg)
                tn_mu = np.mean(tnn_avg)
                tpn_arr.append(tp_mu)
                tnn_arr.append(tn_mu)
                title = 'AvgConfusionMatrix_'+twnd+'_'+method+'_'+cncpt
                cf_mat = np.array([[tn_mu,1-tn_mu],[1-tp_mu,tp_mu]])
                np.set_printoptions(precision=2)
                plt.figure()
                plot_confusion_matrix(cf_mat,classes = ['Other','Fall'],normalize=True,title=title)
                plt.savefig(cncpt+'//'+twnd+'//'+title+'.jpg')
                plt.close()
            acc_e.append(acc_arr)
            ppv_e.append(ppv_arr)
            rec_e.append(rec_arr)
            fsc_e.append(fsc_arr)
            tpn_e.append(tpn_arr)
            tnn_e.append(tnn_arr)
        w = open(cncpt + '//Score_' + cncpt +'_temp.csv','w')
        try:
            writeFinal(w,'Accuracy',acc_e,t_window,methods,True)
            writeFinal(w,'Precision',ppv_e,t_window,methods,True)
            writeFinal(w,'Recall',rec_e,t_window,methods,True)
            writeFinal(w,'F1Score',fsc_e,t_window,methods)
        except Exception as e:
            print(e)
        w.close()
        #The scores for evey time window and method are plotted in a bar graph
        plotScore([acc_e,ppv_e,rec_e,fsc_e],cncpt,t_window=t_window,methods=methods)
        #The average confusion matrix is plotted (avg time window for every method)
        for i in range(0,len(methods)):
            #true positive
            tp_sm = 0
            #true negative
            tn_sm = 0
            for j in range(0,len(t_window)):
                tp_sm += tpn_e[j][i]
                tn_sm += tnn_e[j][i]
            tp_sm = tp_sm/len(t_window)
            tn_sm = tn_sm/len(t_window)
            title = 'Avg Confusion Matrix ' + methods[i] + ' ' + cncpt
            cf_mat = np.array([[tn_sm,1-tn_sm],[1-tp_sm,tp_sm]])
            np.set_printoptions(precision=2)
            plt.figure()
            plot_confusion_matrix(cf_mat,classes = ['Other','Fall'],normalize=True,title=title)
            plt.savefig(cncpt+'//AvgConfusionMatrix_'+methods[i]+'_'+cncpt+'.jpg')
            plt.close()
def main():
    concept = []
    BC_Training(concept)
    BC_Scores(concept)
    
if __name__ == "__main__":
    main()
