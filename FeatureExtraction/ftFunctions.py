# -*- coding: utf-8 -*-
"""
Created on Thu Sep  5 18:12:36 2019

@author: 0169723
"""
import csv
import datetime
from fCalculation import tdom, fdom
from statistics import mode
from statistics import StatisticsError
from createFolder import createFolder
from SFt_List import getSensors, getFeatures


def createHeader(sensorList, ftList,t_stamp):
    final = [[]]
    dif = 0
    h_start = False
    if t_stamp:
        final[0].append('')
        final.append([])
        final[1].append('Timestamp')
        dif = 1
    for sensor in sensorList:
        if t_stamp:
            final[0].append(sensor)
            h_start = False
        for feature in ftList:
            if h_start:
                final[0].append('')
            elif t_stamp:
                h_start = True
            final[0 + dif].append(sensor + feature)
    final[0 + dif].append('Subject')
    final[0 + dif].append('Activity')
    final[0 + dif].append('Trial')
    final[0 + dif].append('Tag')
    return final,dif

#Function used to extract data from a specific sensor and return it as a list
def extractSensor(location,temp):
    sensorData = []
    for row in temp:
        sensorData.append(row[location])
    return sensorData

#Function used to extract and return time from sepcific row        
def getTime(row):
    year = int(row[0][0:4])
    month = int(row[0][5:7])
    day = int(row[0][8:10])
    hour = int(row[0][11:13])
    minute = int(row[0][14:16])
    second = int(row[0][17:19])
    microsecond = int(row[0][20:26])
    return datetime.datetime(year,month,day,hour,minute,second,microsecond)

#Function which calulates features given location of trial csvs, subjects, activities, and trial.
#actn is the number trial and trl is the string
#actn is used for when the tags in the samples are exactly split in half
#in that case actn is used as the overall tag
def features(datafile,finaloc,sub,act,trl,actn,twnd,t_stamp = False):
    tlen = twnd.split('&')
    st1 = float(tlen[0])
    st2 = float(tlen[1])
    #Opens a csv file and puts it into an array 
    csvFile = open(datafile)
    csvArray = []
    for row in csvFile:
        row = row.split(',')
        csvArray.append(row)
    csvFile.close()
    csvArray = [[item.strip('\n') for item in array]for array in csvArray]
    #Obtains Starting and Ending timestamp of trial
    starttime = getTime(csvArray[2])
    finaltime = getTime(csvArray[len(csvArray)-1])
    temp = []
    subSensors = []
    sensorList = getSensors()
    ftList = getFeatures()
    final, dif = createHeader(sensorList, ftList,t_stamp)
    j = 1 + dif
    #To know if a sensor has presented an error:
    i_prev = -1
    #While loop that runs from starttime to finaltime
    while starttime+datetime.timedelta(seconds=st1) <= finaltime:
        #Data is collected within st1 second windows, with the starttime increasing by st2 seconds
        for row in csvArray[2:]:
            if starttime <= getTime(row) and getTime(row) <= starttime+datetime.timedelta(seconds=st1):
                temp.append(row)
        #All data is seperated into individial lists containing only data from a single sensor (i.e. Ankle Accelerometer x-axis)
        try:
            for i in range(len(temp[0])):
                subSensors.append([])
                for row in temp:
                    subSensors[i].append(row[i])
            
            #A new list is added to put calculated data in
            final.append([])
            if t_stamp:
                #The start time of the window is added
                final[j].append(datetime.datetime.strftime(starttime, '%Y-%m-%dT%H:%M:%S.%f'))
            #For loop going though each individual sensor's data
            i_sensor = 0
            for row in subSensors[1:len(sensorList)+1]:
                try:
                    #Converts row into floats
                    nrow = list(map(float, row))
                    #Extracts features
                    features = tdom(nrow,ftList)
                    #Extract frquency features
                    frequency = fdom(nrow,subSensors[0],ftList)
                    #Add features to final array
                    for dat in features:
                        final[j].append(dat)
                    #Add frequency features to final array
                    for dat1 in frequency:
                        final[j].append(dat1)
                except ValueError as e:
                    if i_sensor != i_prev:
                        print('---------Error with ' + sensorList[i_sensor] +': ' + str(e))
                        i_prev = i_sensor
                    for i in range(0,len(ftList)):
                        final[j].append('')
                i_sensor += 1
            #Add Subject,Activity,Trial,and Tag at the end of row
            final[j].append(mode(subSensors[len(sensorList)+1]))
            final[j].append(mode(subSensors[len(sensorList)+2]))
            final[j].append(mode(subSensors[len(sensorList)+3]))
            try:
                final[j].append(mode(subSensors[len(sensorList)+4]))
            except StatisticsError:
                final[j].append(actn)
            j+=1
        #Exception for when the st1 second window exceeds data timestamps
        except Exception as ex:
            if str(ex) == 'list index out of range':
                print('------Possible data absence between timestamps: ')
                nexttime = starttime + datetime.timedelta(seconds = st2)
                print('-----------' +str(starttime)+ ' and ' + str(nexttime))
            else:
                print('---Unexpected error: ' + str(ex))
        #st2 seconds are added for overlapping windowing
        starttime += datetime.timedelta(seconds = st2)
        #temp and subSensor arrays are reset
        temp = []
        subSensors = []
    #A folder and file is created to store new data
    createFolder(finaloc)
    with open (finaloc + sub + act + trl + 'Features'+ twnd + '.csv', 'w') as newDataSet:        
        csvwriter = csv.writer(newDataSet,lineterminator = '\n')
        for row in final:
            csvwriter.writerow(row)
        newDataSet.close()

#A function that joins the different feature files created
def featureJoiner(path,
                  twnd,
                  t_stamp,
                  n_sub=[1,17],
                  n_act=[1,11],
                  n_trl=[1,3]):
    f_row = 1
    if t_stamp:
        f_row = 2
    f_name = 'Features' + twnd + '.csv'
    f_flg = True
    w = open(path + f_name, 'w')
    try:
        for i  in range(n_sub[0],n_sub[1]+1):
            sub = 'Subject' + str(i)
            for j in range(n_act[0],n_act[1]+1):
                act = 'Activity' + str(j)
                for k in range(n_trl[0],n_trl[1]+1):
                    trl = 'Trial' + str(k)
                    f_path = path + sub + '\\' + act + '\\' + trl + '\\'
                    r = open(f_path + sub+act+trl+'Features'+twnd+'.csv','r')
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
    except Exception as e:
        print('--An unexpected error ocurred while writing ' + f_name +' :')
        print('-----' + str(e))
    w.close()
