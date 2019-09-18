# -*- coding: utf-8 -*-
"""
Created on Fri Jan 11 14:27:56 2019

@author: José Pablo
"""

from PIL import Image
import numpy as np
from numpy import genfromtxt
import os
from createFolder import createFolder
from progressBar import progressBar
import sys

#A function to replace dashes in the timestamps with colons
def tstGT(st):
    st = st.replace('_',':')
    return st[:-6]

#A function to make a 20x20 resize to csv containing the image features
def resCSV(file):
    #An image is generated from the csv file
    g = open(file,'r')
    temp = genfromtxt(g, delimiter = ',')
    g.close()
    arr = np.array(temp,dtype=np.float32)
    rzero = np.min(arr)
    arr = arr + np.abs(rzero)
    r255 = np.amax(arr)
    if r255 != 0:
        fcon = 255/r255
        arr = arr*fcon
    img = Image.fromarray(arr).convert('RGB')    
    img = img.resize((20, 20), Image.ANTIALIAS)
    img.load()
    data = np.asarray( img, dtype=np.float32)
    narr = []
    for i in range(0,20):
        #rows
        tmp = []
        for j in range(0,20):
            #columns
            tmp.append(data[i][j][0])
        narr.append(tmp)
    return narr

#A function to get the magnitude from each change, from v and u
def sqrd(arru, arrv):
    tmp1 = np.square(arru,dtype=np.float32)
    tmp2 = np.square(arru,dtype=np.float32)
    tmp = np.add(tmp1,tmp2,dtype=np.float32)
    arrf = np.sqrt(tmp,dtype=np.float32)
    return(arrf)

def camOF_joiner(gral,
                 rs_path,
                 n_sub=[1,17],
                 n_act=[1,11],
                 n_trl=[1,3],
                 n_cam=[1,2]):
  cmr = []
  interrupt = False
  for cam in n_cam:
    cmr.append('Camera'+str(cam)+'_OF_UZ//')
  for i in range(n_sub[0],n_sub[1]+1):
      if interrupt:
          break
      sub = 'Subject' + str(i)
      print(sub)
      for j in range(n_act[0],n_act[1]+1):
          if interrupt:
              break
          act = 'Activity' + str(j)
          print('S'+str(i)+'--'+act)
          for k in range(n_trl[0],n_trl[1]+1):
              if interrupt:
                  break
              trl = 'Trial' + str(k)
              print('S'+str(i)+'-A'+str(j)+'--'+trl)
              path = gral+sub+'//'+act+'//'+trl+'//'+sub+act+trl+cmr[0]
              #path = gral+trl+'//'+sub+act+trl+cmr[0]
              path2 = gral+sub+'//'+act+'//'+trl+'//'+sub+act+trl+cmr[1]
              if os.path.exists(path) and os.path.exists(path2):
                  files = os.listdir(path)
                  files2 = os.listdir(path2)
                  if len(files)==len(files2):
                      p = 0
                      n_path = rs_path+sub+'//'+act+'//'
                      createFolder(n_path)
                      n_file = 'CameraFeatures'+sub+act+trl+'.csv'
                      print('----------Writing...')
                      w = open(n_path+n_file,'w')
                      try:
                          w.write('Timestamp')
                          for z in range(n_cam[0],n_cam[1]+1):
                              for q in range(0,20):
                                  for r in range(0,20):
                                      w.write(',C'+str(z)+'('+str(q)+';'+str(r)+')')
                          w.write(',Subject,Activity,Trial')
                          print('------------Joining ' + str(len(files)) + ' files')
                          while p < len(files):
                              if p % 2 == 0:
                                  npath = path + files[p]
                                  npath2 = path2 + files[p]
                                  tst = tstGT(files[p])
                                  arr1 = resCSV(npath)
                                  sar1 = resCSV(npath2)
                                  p+=1
                                  npath = path + files[p]
                                  npath2 = path2 + files[p]
                                  arr2 = resCSV(npath)
                                  sar2 = resCSV(npath2)
                                  arrf = sqrd(arr1,arr2)
                                  sarf = sqrd(sar1,sar2)
                                  w.write('\n'+tst)
                                  for q in range(0,20):
                                      for r in range(0,20):
                                          w.write(','+str(arrf[i][j]))
                                  for q in range(0,20):
                                      for r in range(0,20):
                                          w.write(','+str(sarf[i][j]))
                                  w.write(','+str(i)+','+str(j)+','+str(k))
                                  progressBar('-------------Progress',p,len(files),width=2)
                              p+=1
                      except KeyboardInterrupt:
                          print("\nThe program has been interrupted.")
                          interrupt = True
                      except Exception as e:
                          print('-----------Unexpected error: ' + str(e))
                      w.close()
                      if not interrupt:
                          print('\n------------'+n_file+' has been successfully created.' )
                  else:
                      print('------------Images from paths ' + path +' and ' +path2 + ' do not fit')

def main():
    OF_path = ''
    resize_path = ''
    camOF_joiner(OF_path,resize_path)
    print('End of task')
    
if __name__ == "__main__":
    main()
