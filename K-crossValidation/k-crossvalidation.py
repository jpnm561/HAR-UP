# -*- coding: utf-8 -*-
"""
Created on Thu Nov  7 19:43:12 2019

@author: JosePablo
"""
import pandas as pd
from sklearn.model_selection import KFold

def k_crossFiles(concept,
                 t_window = ['1&0.5','2&1','3&1.5'],
                 K=10):
    for cncpt in concept:
        print(cncpt)
        for twnd in t_window:
            print('---%s' % twnd)
            path = '%s//%s//' % (cncpt, twnd)
            training = pd.read_csv('%s//SelectedFTS_%s_%s.csv' % (path,twnd,cncpt))
            header = []
            for i in range(0,len(training.columns)):
                header.append(training.columns[i])
            
            training_set = training.values
            kfold = KFold(K, True, 1)
            # enumerate splits
            i = 1
            for train, test in kfold.split(training_set):
                print('------Fold %s' % i)
                wtr = open(path + 'SelectedFeatures_'+twnd+'_'+cncpt+'_train'+str(i)+'.csv', 'w')
                wts = open(path + 'SelectedFeatures_'+twnd+'_'+cncpt+'_test'+str(i)+'.csv', 'w')
                try:
                    bnd = True
                    for feature in header:
                        if bnd:
                            wtr.write(feature)
                            wts.write(feature)
                            bnd = False
                        else:
                            wtr.write(',' + feature)
                            wts.write(',' + feature)   
                    wtr.write('\n')
                    wts.write('\n')
                    for j in range(0,training_set[train].shape[0]-1):
                        for k in range(0,training_set[train].shape[1]-1):
                            wtr.write(str(training_set[train][j][k]) + ',')
                        wtr.write(str(training_set[train][j][training_set[train].shape[1]-1]) + '\n')
                    for k in range(0,training_set[train].shape[1]-1):
                        wtr.write(str(training_set[train][training_set[train].shape[0]-1][k]) + ',')
                    wtr.write(str(training_set[train][training_set[train].shape[0]-1][training_set[train].shape[1]-1]))
                    
                    for j in range(0,training_set[test].shape[0]-1):
                        for k in range(0,training_set[test].shape[1]-1):
                            wts.write(str(training_set[test][j][k]) + ',')
                        wts.write(str(training_set[test][j][training_set[test].shape[1]-1]) + '\n')
                    for k in range(0,training_set[test].shape[1]-1):
                        wts.write(str(training_set[test][training_set[test].shape[0]-1][k]) + ',')
                    wts.write(str(training_set[test][training_set[test].shape[0]-1][training_set[test].shape[1]-1]))
                except Exception as e:
                    print('----Unexpected error ' + str(e))
                wtr.close()
                wts.close()
                i += 1

def main():
    concept = []
    k_crossFiles(concept)
    print('\nEnd of task')

    
if __name__=="__main__":
    main()
    
