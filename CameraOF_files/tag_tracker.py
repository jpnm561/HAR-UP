# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 23:04:33 2019

@author: JosePablo
"""

import os
from createFolder import createFolder
import sys
from progressBar import progressBar

"""
----------------------------------------------------------------------------
Functions
----------------------------------------------------------------------------
"""

def readDBase(path):
    r = open(path,'r')
    txt = r.read()
    r.close()
    d_base = txt.split('\n')
    return d_base

def relData(arr):
    n_arr = []
    for i in range(2,len(arr)):
        ln = arr[i].split(',')
        if len(ln) > 4:
            #timestamp,subject,activity,trial,tag
            tmp = [ln[0],ln[-4],ln[-3],ln[-2],ln[-1]]
            n_arr.append(tmp)
    return n_arr

def index_val(arr,idx,sub,act,trl):
    val = False
    if idx != len(arr):
        if int(arr[idx][1])==sub and int(arr[idx][2])==act and int(arr[idx][3])==trl:
            val = True
    return val

def tag_track(gral = '',
                 tag_path,
                 file_tags,
                 n_sub=[1,17],
                 n_act=[1,11],
                 n_trl=[1,3]):
  interrupt = False
  d_base = relData(readDBase(file_tags))
  #to store the index in wich a certain trial begins
  db_i = 0
  for i in range(n_sub[0],n_sub[1]+1):
      if interrupt:
          break
      sub = 'Subject' + str(i)
      print(sub)
      while int(d_base[db_i][1]) < i:
          db_i += 1
          if db_i == len(d_base):
              print(sub + ' was not found')
              interrupt = True
              break
      for j in range(n_act[0],n_act[1]+1):
          if interrupt:
              break
          act = 'Activity' + str(j)
          print('S'+str(i)+'--'+act)
          flg_out = False
          while int(d_base[db_i][2]) < j:
              db_i += 1
              if (int(d_base[db_i][1]) > i):
                  flg_out = True
              elif  db_i == len(d_base):
                  interrupt = True
              if flg_out:
                  print(sub+' '+act+' was not found')
                  break
          for k in range(n_trl[0],n_trl[1]+1):
              trl = 'Trial' + str(k)
              print('S'+str(i)+'-A'+str(j)+'--'+trl)
              flg_out = False
              while int(d_base[db_i][3]) < k:
                  db_i += 1
                  if (int(d_base[db_i][1]) > i) or (int(d_base[db_i][2]) > i):
                      flg_out = True
                  elif  db_i == len(d_base):
                      break              
                  if flg_out:
                      print(sub+' '+act+' '+trl+' was not found')
                      break
              if interrupt:
                  break
              path = gral+sub+'//'+act+'//'+sub+act+trl+'CameraResizedOF_notag.csv'
              n_path = tag_path+sub+'//'+act+'//'
              createFolder(n_path)
              n_file = sub+act+trl+'CameraResizedOF.csv'
              if os.path.exists(path):
                  trl_data = readDBase(path) 
                  w = open(n_path+n_file,'w')
                  try:
                      w.write(trl_data[0] + ',Tag')
                      #An array in which to store timestamps that have no pair in a trial
                      unpaired = []
                      for p in range(1,len(trl_data)):
                          progressBar('-------Progress',p,len(trl_data)-1)
                          ln = trl_data[p].split(',')
                          db_tmp = db_i
                          tst_flg = True
                          while index_val(d_base,db_tmp,i,j,k):
                              #current timestamp is compared with the tag's timestamp
                              if ln[0] == d_base[db_tmp][0]:
                                  w.write('\n' + trl_data[p]+','+d_base[db_tmp][4])
                                  tst_flg = False
                                  break
                              db_tmp += 1
                          if tst_flg:
                              unpaired.append(tst)
                  except KeyboardInterrupt:
                      print("\nThe program has been interrupted.")
                      interrupt = True
                  except Exception as e:
                      print('\n-----------Unexpected error: ' + str(e))
                  w.close()
                  if not interrupt:
                      state=' successfully'
                      if len(unpaired)>0:
                          state=''
                          print('--------Warning, unpaired time stamps: ')
                          print(unpaired)
                      print('-------File'+state+' created.')

def fileJoiner(path,
                  n_sub=[1,17],
                  n_act=[1,11],
                  n_trl=[1,3]):
    f_row = 1
    f_name = 'CameraResizedOF.csv'
    f_flg = True
    p=0
    n_files=(n_sub[1]+1-n_sub[0])*(n_act[1]+1-n_act[0])*(n_trl[1]+1-n_trl[0])
    w = open(path + f_name, 'w')
    try:
        for i  in range(n_sub[0],n_sub[1]+1):
            sub = 'Subject' + str(i)
            for j in range(n_act[0],n_act[1]+1):
                act = 'Activity' + str(j)
                for k in range(n_trl[0],n_trl[1]+1):
                    trl = 'Trial' + str(k)
                    f_path = path + sub + '\\' + act + '\\'
                    progressBar('--Joining files',p,n_files-1)
                    r = open(f_path+sub+act+trl+'CameraResizedOF.csv','r')
                    txt = r.read()
                    r.close()
                    file = txt.split('\n')
                    start = f_row
                    if f_flg:
                        w.write(file[0])
                        if f_row == 2:
                            w.write('\n' + file[1])
                        f_flg = False
                    for row in file[start:]:
                        q = row.split(',')
                        if (q[0]!='') and (q[-1]!=''):
                            w.write('\n'+row)
                    p+=1
    except KeyboardInterrupt:
        print("\n--The program has been interrupted.")
    except Exception as e:
        print('\n--Unexpected error: ' + str(e))
    w.close()

"""
----------------------------------------------------------------------------
End of functions
----------------------------------------------------------------------------
"""

def main():
    resize_path = ''
    tag_resize_path = ''
    file_with_tags = 'CompleteDataSet.csv'
    tag_track(resize_path, tag_resize_path, file_with_tags)
    fileJoiner(tag_resize_path)
    print('End of task')
if __name__ == "__main__":
    main()
