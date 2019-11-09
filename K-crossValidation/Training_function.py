# -*- coding: utf-8 -*-
"""
Created on Thu Nov  7 10:23:15 2019

@author: HAR-UP
"""

from sklearn import svm
from sklearn.ensemble import RandomForestClassifier as RndFC
from sklearn.neural_network import MLPClassifier as ffp
from sklearn.neighbors import KNeighborsClassifier as KNN
import pandas as pd
from sklearn import metrics as met


def training(concept,
             t_window = ['1&0.5','2&1','3&1.5'],
             methods = ['RF','SVM', 'MLP', 'KNN'],
             K=10):
    
    for cncpt in concept:
        print(cncpt)
        
        for twnd in t_window:
            print('--%s' % twnd)    
            path = '%s//%s//' % (cncpt,twnd)
            #Each fold's accuracy is stored
            acc_k = []
            for k in range(1,K+1):
                print('-----Fold %d:' % k)
                
                #Training and testing sets are opened with pandas
                training_set = pd.read_csv('%sSelectedFeatures_%s_%s_train%d.csv'%(path,twnd,cncpt,k))
                testing_set = pd.read_csv('%sSelectedFeatures_%s_%s_test%d.csv'%(path,twnd,cncpt,k))
                
                #Training data set is split into inputs (X) and outputs (Y)
                training_set_X = training_set.drop(training_set.columns[-1],axis=1)
                training_set_Y = training_set[training_set.columns[-1]]
                
                #Testing data is split
                testing_set_X = testing_set.drop(testing_set.columns[-1],axis=1)
                expected_output = testing_set[testing_set.columns[-1]].values
                
                #Each method's accuracy is stored
                acc_method = []
                for method in methods:
                    if method == 'RF':
                        classifier = RndFC(n_estimators=100)
                    elif method == 'SVM':
                        classifier = svm.SVC(gamma='auto', kernel = 'poly')
                    elif method == 'MLP': 
                        classifier = ffp()
                    else:
                        classifier = KNN()
                    classifier.fit(training_set_X, training_set_Y)
                    
                    #The classifier is tested
                    estimates = classifier.predict(testing_set_X)
                    accuracy = met.accuracy_score(expected_output,estimates)
                    print('-----------%s Accuracy: %f' % (method, accuracy))
                    acc_method.append(accuracy)
                acc_k.append(acc_method)
            print('---%s scores:' % twnd)
            for i in range(0,len(methods)):
                avg_accuracy = 0
                for k in range(0,K):
                    avg_accuracy += acc_k[k][i]
                avg_accuracy = avg_accuracy/K
                print('------%s Avg. Accuracy: %f' %(methods[i],avg_accuracy))

def main():
    concept = []
    training(concept)
    print('\nEnd of task')

    
if __name__=="__main__":
    main()
