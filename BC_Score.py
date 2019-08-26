# -*- coding: utf-8 -*-
"""
Created on Tue Feb 19 19:41:36 2019

@author: José Pablo
"""


from sklearn import metrics as met
import numpy as np
import itertools
import matplotlib.pyplot as plt

"""
Confusion matrix code taken from scikit-learn.org
https://scikit-learn.org/stable/auto_examples/model_selection/plot_confusion_matrix.html#sphx-glr-auto-examples-model-selection-plot-confusion-matrix-py
"""
def plot_confusion_matrix(cm,classes,normalize=True,title='Confusion matrix',cmap=plt.cm.Blues):
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:,np.newaxis]
    plt.imshow(cm,interpolation='nearest',cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks,classes,rotation=45)
    plt.yticks(tick_marks,classes)
    fmt = '.2f'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]),range(cm.shape[1])):plt.text(j,i,format(cm[i,j],fmt),
                                        horizontalalignment='center',
                                        color='white' if cm[i,j] > thresh else 'black')
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.tight_layout()

def write_score(w, score, wk_arr,l_flg = False):
    w.write(score + '\n')
    for i in range(0, len(wk_arr)):
        w.write(str(wk_arr[i]))
        if i < len(wk_arr) - 1:
            w.write(',')
    w.write('\n')
    mu = np.mean(wk_arr)
    sig = np.std(wk_arr)
    w.write('Mean,' + str(mu) + '\n')
    w.write('DS,' + str(sig))
    if l_flg:
        w.write('\n')
    return [mu,sig]

#An array with the time-windows that will be used
fldrs = ['1&0.5', '2&1', '3&1.5']
#An array with the experiments
concept = ['IMU','Head', 'IR_Vision']
#An array with the methods that will be used
typ = ['RF','SVM','MLP','KNN']

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
    for sup in range(0, len(fldrs)):  #time window
        print('--' + fldrs[sup])
        acc_arr = []
        ppv_arr = []
        fsc_arr = []
        rec_arr = []
        tpn_arr = []
        tnn_arr = []
        for f in range(0,len(typ)):  #method
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
                doc = cncpt+'//'+fldrs[sup]+'//'+typ[f]+'//Resultado_'+fldrs[sup]+'_'+typ[f]+'_'+str(i)+'.csv'
                r = open(doc,'r')
                txt = r.read()
                r.close()
                base = txt.split('\n')
                for j in range(1,len(base)):
                    ln = str(base[j])
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
                    print('There were no falls in: ' + cncpt + '-' + fldrs[sup] + '-' + str(j + 1))
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
                
            odoc = cncpt+'//'+fldrs[sup]+'//Score_'+fldrs[sup]+'_'+typ[f]+'.csv'
            w = open(odoc, 'w')
            try:
                acc_arr.append(write_score(w,'Accuracy',acc_avg,True))
                ppv_arr.append(write_score(w,'Precision',ppv_avg,True))
                rec_arr.append(write_score(w,'Recall',rec_avg,True))
                fsc_arr.append(write_score(w,'F1Score',fsc_avg))
                print('----' + typ[f] + ' ' + fldrs[sup] + ' done')
            except Exception as e:
                print('----ERROR: ' + str(e))
            w.close()
            #Plotting the confusion matrix
            tp_mu = np.mean(tpn_avg)
            tn_mu = np.mean(tnn_avg)
            tpn_arr.append(tp_mu)
            tnn_arr.append(tn_mu)
            title = 'AvgConfusionMatrix_'+fldrs[sup]+'_'+typ[f]+'_'+cncpt
            cf_mat = np.array([[tn_mu,1-tn_mu],[1-tp_mu,tp_mu]])
            np.set_printoptions(precision=2)
            plt.figure()
            plot_confusion_matrix(cf_mat,classes = ['Other','Fall'],normalize=True,title=title)
            plt.savefig(cncpt+'//'+fldrs[sup]+'//'+title+'.jpg')
            plt.close()
        acc_e.append(acc_arr)
        ppv_e.append(ppv_arr)
        rec_e.append(rec_arr)
        fsc_e.append(fsc_arr)
        tpn_e.append(tpn_arr)
        tnn_e.append(tnn_arr)
    w = open(cncpt + '//Score_' + cncpt +'_temp.csv','w')
    try:
        w.write('Accuracy\n')
        w.write(',Random Forest,,SVM,,MLP,,KNN,')
        for i in range(0,len(fldrs)):
            w.write('\n' + fldrs[i])
            for j in range(0,len(typ)):
                for k in range(0,2):
                    w.write(',' + str(acc_e[i][j][k]))
        w.write('\nPrecision\n')
        w.write(',Random Forest,,SVM,,MLP,,KNN,')
        for i in range(0,len(fldrs)):
            w.write('\n' + fldrs[i])
            for j in range(0,len(typ)):
                for k in range(0,2):
                    w.write(',' + str(ppv_e[i][j][k]))
        w.write('\nRecall\n')
        w.write(',Random Forest,,SVM,,MLP,,KNN,')
        for i in range(0,len(fldrs)):
            w.write('\n' + fldrs[i])
            for j in range(0,len(typ)):
                for k in range(0,2):
                    w.write(',' + str(rec_e[i][j][k]))
        w.write('\nF1Score\n')
        w.write(',Random Forest,,SVM,,MLP,,KNN,')
        for i in range(0,len(fldrs)):
            w.write('\n' + fldrs[i])
            for j in range(0,len(typ)):
                for k in range(0,2):
                    w.write(',' + str(fsc_e[i][j][k]))
    except Exception as e:
        print(e)
    w.close()
    #For each method
    for i in range(0,len(typ)):
        #twind
        tp_sm = 0
        tn_sm = 0
        #For each time-window
        for j in range(0,len(fldrs)):
            tp_sm += tpn_e[j][i]
            tn_sm += tnn_e[j][i]
        tp_sm = tp_sm/len(fldrs)
        tn_sm = tn_sm/len(fldrs)
        title = 'Avg Confusion Matrix ' + typ[i] + ' ' + cncpt
        cf_mat = np.array([[tn_sm,1-tn_sm],[1-tp_sm,tp_sm]])
        np.set_printoptions(precision=2)
        plt.figure()
        plot_confusion_matrix(cf_mat,classes = ['Other','Fall'],normalize=True,title=title)
        plt.savefig(cncpt+'//AvgConfusionMatrix_'+typ[i]+'_'+cncpt+'.jpg')
        plt.close()
print('End of program')
