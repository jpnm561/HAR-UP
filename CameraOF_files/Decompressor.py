# -*- coding: utf-8 -*-
"""
Created on Mon Nov 26 12:38:12 2018
@author: José Pablo
"""

import zipfile as zf
import os
import shutil
from createFolder import createFolder
from progressBar import progressBar

#A function that unzips folders in a direcory
def UnzipFolders(o_dir,n_dir,
              n_sub=[1,17],
              n_act=[1,11],
              n_trl=[1,3],
              n_cam=[1,2]):
    #Subjects
    for i in range(n_sub[0],n_sub[1]+1):
        sub = 'Subject' + str(i)
        print('--%s' % (sub))
        #Activities
        for j in range(n_act[0],n_act[1]+1):
            act = 'Activity' + str(j)
            print('--S%s--%s' % (str(i),act))
            #Trials        
            for k in range(n_trl[0],n_trl[1]+1):
                trl = 'Trial' + str(k)
                print('--S%s--A%s--%s' % (str(i),str(j),trl))
                gral = sub+'//'+act+'//'+trl+'//'
                #Cameras
                for l in range(n_cam[0],n_cam[1]+1):
                    directory = o_dir + gral
                    path = n_dir + gral +sub+act+trl+ 'Camera' + str(l) + '_OF_temp'
                    createFolder(path)
                    try:
                        p = 0
                        progressBar('------Camera'+str(l),p,len(os.listdir(directory)))
                        for filen in os.listdir(directory):
                            zipf = zf.ZipFile(directory + '//' + filen)
                            zipf.extractall(path)
                            zipf.close()
                            p+=1
                            progressBar('------Camera'+str(l),p,len(os.listdir(directory)))
                    except:
                        print('--------The following direcory was not found: ' + directory)
                #print('--Unzipped:' + sub + act + trl)

#A function that deleats temporal files creaeted during the process
def DeleateFolder(n_dir,
              n_sub=[1,17],
              n_act=[1,11],
              n_trl=[1,3],
              n_cam=[1,2]):
    print('Deleating temporal files')
    p = 0
    q = (n_sub[1] + 1 - n_sub[0])*(n_act[1] + 1 - n_act[0])*(n_trl[1] + 1 - n_trl[0])*(n_cam[1] + 1 - n_cam[0])
    progressBar('--Progress',p,q)
    #Subjects
    for i in range(n_sub[0],n_sub[1]+1):
        sub = 'Subject' + str(i)
        #Activities
        for j in range(n_act[0],n_act[1]+1):
            act = 'Activity' + str(j)
            #Trials        
            for k in range(n_trl[0],n_trl[1]+1):
                trl = 'Trial' + str(k)
                gral = sub+'//'+act+'//'+trl+'//'
                #Cameras
                for l in range(n_cam[0],n_cam[1]+1):
                    path = n_dir + gral +sub+act+trl+ 'Camera' + str(l) + '_OF_temp'
                    try:
                        shutil.rmtree(path)
                    except:
                        print('An error ocurred when deleating: ' + path)
                    p+=1
                    progressBar('--Progress',p,q)

#a function that decompresses the folders 
def Decompressor(o_dir,n_dir,
              n_sub=[1,17],
              n_act=[1,11],
              n_trl=[1,3],
              n_cam=[1,2]):
    #Unzipping the outer folders
    print('Unzipping outer folders: ')
    UnzipFolders(o_dir, n_dir, n_sub, n_act, n_trl, n_cam)
    print('Unzipping optical flow files: ')
    #Subjects
    for i in range(n_sub[0],n_sub[1]+1):
        sub = 'Subject' + str(i)
        print('--%s' % (sub))
        #Activities
        for j in range(n_act[0],n_act[1]+1):
            act = 'Activity' + str(j)
            print('--S%s--%s' % (str(i),act))
            #Trials        
            for k in range(n_trl[0],n_trl[1]+1):
                trl = 'Trial' + str(k)
                print('--S%s--A%s--%s' % (str(i),str(j),trl))
                gral = sub+'//'+act+'//'+trl+'//'+sub+act+trl
                #Cameras
                for l in range(n_cam[0],n_cam[1]+1):
                    directory = n_dir + gral + 'Camera' + str(l) + '_OF_temp'
                    path = n_dir + gral + 'Camera' + str(l) + '_OF_UZ'
                    createFolder(path)
                    try:
                        p = 0
                        progressBar('------Camera'+str(l),p,len(os.listdir(directory)))
                        for filen in os.listdir(directory):
                            zipf = zf.ZipFile(directory + '//' + filen)
                            zipf.extractall(path)
                            zipf.close()
                            p+=1
                            progressBar('------Camera'+str(l),p,len(os.listdir(directory)))
                    except:
                        print('The following direcory was not found: ' + directory)
                #print('-----Unzipped:' + sub + act + trl)
    DeleateFolder(n_dir, n_sub, n_act, n_trl, n_cam)

def main():
    original_directory = ''
    new_directory = ''
    Decompressor(original_directory,new_directory)
    print('End of task')

if __name__=="__main__":
    main()
