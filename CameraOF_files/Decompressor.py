# -*- coding: utf-8 -*-
"""
Created on Mon Nov 26 12:38:12 2018
@author: José Pablo
"""

import zipfile as zf
import os
from createFolder import createFolder

#A function that unzips folders in a direcory
def UnzipFolders(o_dir,n_dir,
              n_sub=[1,17],
              n_act=[1,11],
              n_trl=[1,3],
              n_cam=[1,2]):
    #Subjects
    for i in range(n_sub[0],n_sub[1]+1):
        sub = 'Subject' + str(i)
        print(sub + ':')
        #Activities
        for j in range(n_act[0],n_act[1]+1):
            act = 'Activity' + str(j)
            print('\t' + act + ':')
            #Trials        
            for k in range(n_trl[0],n_trl[1]+1):
                trl = 'Trial' + str(k)
                print('\t\t' + trl + ':')
                gral = sub+'//'+act+'//'+trl+'//'
                #Cameras
                for l in range(n_cam[0],n_cam[1]+1):
                    directory = o_dir + gral
                    path = n_dir + gral +sub+act+trl+ 'Camera' + str(l) + '_OF'
                    createFolder(path)
                    try:
                        for filen in os.listdir(directory):
                            zipf = zf.ZipFile(directory + '//' + filen)
                            zipf.extractall(path)
                            zipf.close()
                    except:
                        print('The following direcory was not found: ' + directory)
                print('\t\t\t Unzipped:' + sub + act + trl)

#a function that decompresses the folders 
def Decompressor(o_dir,n_dir,
              n_sub=[1,17],
              n_act=[1,11],
              n_trl=[1,3],
              n_cam=[1,2]):
    #Subjects
    for i in range(n_sub[0],n_sub[1]+1):
        sub = 'Subject' + str(i)
        print(sub + ':')
        #Activities
        for j in range(n_act[0],n_act[1]+1):
            act = 'Activity' + str(j)
            print('\t' + act + ':')
            #Trials        
            for k in range(n_trl[0],n_trl[1]+1):
                trl = 'Trial' + str(k)
                print('\t\t' + trl + ':')
                gral = sub+'//'+act+'//'+trl+'//'+sub+act+trl
                #Cameras
                for l in range(n_cam[0],n_cam[1]+1):
                    directory = o_dir + gral + 'Camera' + str(l) + '_OF'
                    path = n_dir + gral + 'Camera' + str(l) + '_OF_UZ'
                    createFolder(path)
                    try:
                        for filen in os.listdir(directory):
                            zipf = zf.ZipFile(directory + '//' + filen)
                            zipf.extractall(path)
                            zipf.close()
                    except:
                        print('The following direcory was not found: ' + directory)
                print('\t\t\t Unzipped:' + sub + act + trl)

def main():
    original_directory = ''
    new_directory = ''
    UnzipFolders(original_directory,new_directory)
    Decompressor(new_directory,new_directory)
    print('End of task')

if __name__=="__main__":
    main()
