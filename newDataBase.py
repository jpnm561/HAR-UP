# -*- coding: utf-8 -*-
"""
Created on Sun Feb 17 22:02:20 2019

@author: José Pablo
"""

import os
import numpy as np

"""
----------------------------------------------------------------------------------------------------
Functions
----------------------------------------------------------------------------------------------------
"""

#A method that doubles the falls and takes away (randomly) 2/3 of other trials
def incrementFalls(concept, t_window=['1&0.5','2&1','3&1.5']):
    for cncpt in concept:
        print(cncpt)
        for twnd in t_window:
            print('--' + twnd)
            doc = cncpt + '_bin_' + twnd + '.csv'
            if os.path.exists(doc):
                r = open(doc, 'r')
                txt = r.read()
                r.close()
                d_base = txt.split('\n')
                print('-----Writing...')
                w = open(cncpt + '_bmod_' + twnd + '.csv', 'w')
                try:
                    w.write(d_base[0])
                    sub = 1
                    act = 1
                    trl = 1
                    for i in range(1,len(dbase)):
                        ln = dbase[i].split(',')
                        #We make sure we don't have empty lines
                        if (len(ln) > 4) and (ln[0] != '') and (ln[0] != ' '):
                            #We double every fall (tag = 1)
                            if int(ln[-1]) == 1:
                                w.write('\n' + d_base[i])
                                w.write('\n' + d_base[i])
                            else:
                                #We check if we're dealing with a new activity or subject
                                if (int(ln[-3]) != act) or (int(ln[-4]) != sub):
                                    sub = int(ln[-4])
                                    act = int(ln[-3])
                                    #A random trial is selected for said subject and activity
                                    trl = np.random.random_integers(1,3)
                                    #Because subject 8 activity 11 only  consists of trial 1
                                    if (sub == 8) and (act == 11):
                                        trl = 1
                                #While we're dealing with the desired trial, we write it
                                if trl == int(ln[-2]):
                                        w.write('\n' + d_base[i])
                        else:
                            print('----' + str(i + 1) + '/' + str(len(d_base)))
                    print('-----...done')
                except Exception as e:
                    print('-----Unexpected error: ' + str(e))
                w.close()
            else:
                print('----The specified file could not be found')

"""
----------------------------------------------------------------------------------------------------
End of functions
----------------------------------------------------------------------------------------------------
"""

def main():
    concept = []
    incrementFalls(concept)
    print('End of task')
if __name__ == "__main__":
    main()
