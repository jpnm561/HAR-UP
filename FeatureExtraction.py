# -*- coding: utf-8 -*-
"""
Created on Tue Jul 31 11:44:19 2018

Updated on Mon Sep  2 14:46:57 2019

@author: Nestor Santiago
"""

import csv
import datetime
import os
from fCalculation import tdom, fdom
from statistics import mode
from statistics import StatisticsError

def getSensors():
    sensorList = [ 'AnkleAccelerometer: x-axis (g)',
           'AnkleAccelerometer: y-axis (g)',
           'AnkleAccelerometer: z-axis (g)',
           'AnkleAngularVelocity: x-axis (deg/s)',
           'AnkleAngularVelocity: y-axis (deg/s)',
           'AnkleAngularVelocity: z-axis (deg/s)',
           'AnkleLuminosity: illuminance (lx)', 
           'RightPocketAccelerometer: x-axis (g)',
           'RightPocketAccelerometer: y-axis (g)',
           'RightPocketAccelerometer: z-axis (g)',
           'RightPocketAngularVelocity: x-axis (deg/s)',
           'RightPocketAngularVelocity: y-axis (deg/s)',
           'RightPocketAngularVelocity: z-axis (deg/s)',
           'RightPocketLuminosity: illuminance (lx)',
           'BeltAccelerometer: x-axis (g)',
           'BeltAccelerometer: y-axis (g)',
           'BeltAccelerometer: z-axis (g)',
           'BeltAngularVelocity: x-axis (deg/s)',
           'BeltAngularVelocity: y-axis (deg/s)',
           'BeltAngularVelocity: z-axis (deg/s)',
           'BeltLuminosity: illuminance (lx)',
           'NeckAccelerometer: x-axis (g)',
           'NeckAccelerometer: y-axis (g)',
           'NeckAccelerometer: z-axis (g)',
           'NeckAngularVelocity: x-axis (deg/s)',
           'NeckAngularVelocity: y-axis (deg/s)',
           'NeckAngularVelocity: z-axis (deg/s)',
           'NeckLuminosity: illuminance (lx)',
           'WristAccelerometer: x-axis (g)',
           'WristAccelerometer: y-axis (g)',
           'WristAccelerometer: z-axis (g)',
           'WristAngularVelocity: x-axis (deg/s)',
           'WristAngularVelocity: y-axis (deg/s)',
           'WristAngularVelocity: z-axis (deg/s)',
           'WristLuminosity: illuminance (lx)',
           'BrainSensor',
           'Infrared1',
           'Infrared2',
           'Infrared3',
           'Infrared4',
           'Infrared5',
           'Infrared6']
    return sensorList

def getFeatures():
    ftList = ['Mean',
        'StandardDeviation',
        'RootMeanSquare',
        'MaximalAmplitude',
        'MinimalAmplitude',
        'Median',
        'Number of zero-crossing',
        'Skewness',
        'Kurtosis',
        'First Quartile',
        'Third Quartile',
        'Autocorrelation',
        'Energy'
        ] 
    return ftList

def createHeader(sensorList, ftList):
    final = [[]]
    for sensor in sensorList:
        for feature in ftList:
            final[0].append(sensor + feature)
    final[0].append('Subject')
    final[0].append('Activity')
    final[0].append('Trial')
    final[0].append('Tag')
    return final

#Function creates a folder given directory
def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)

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
    #return datetime.datetime(year,month,day,hour,minute,second)

#Function which calulates features given location of trial csvs, subjects, activities, and trial.
#actn is the number trial and trl is the string
#actn is used for when the tags in the samples are exactly split in half
#in that case actn is used as the overall tag
def features(datafile,finaloc,sub,act,trl,actn,twnd):
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
    final = createHeader(sensorList, ftList)
    j = 1
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
            #The start time of the window is added
            #final[j].append(datetime.datetime.strftime(starttime, '%Y-%m-%dT%H:%M:%S.%f'))
            #For loop going though each individual sensor's data
            for row in subSensors[1:len(sensorList)+1]:
                try:
                    #Converts row into floats
                    nrow = list(map(float, row))
                    #Extracts features
                    features = tdom(nrow)
                    #Extract frquency features
                    frequency = fdom(nrow,subSensors[0])
                    #Add features to final array
                    for dat in features:
                        final[j].append(dat)
                    #Add frequency features to final array
                    for dat1 in frequency:
                        final[j].append(dat1)
                except ValueError as e:
                    print('Error: ' + str(e))
                    for i in range(0,len(ftList)):
                        final[j].append('')
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
            print('Error' + str(ex))
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

#Will run through subjects,activities,and trials inputted
def extraction(loc1,loc2,
               n_sub=[1,17],
               n_act=[1,11],
               n_trl=[1,3],
               t_window = ['1&0.5','2&1','3&1.5']):
    for twnd in t_window:
        for i  in range(n_sub[0],n_sub[1]+1):
            sub = 'Subject' + str(i)
            for j in range(n_act[0],n_act[1]+1):
                act = 'Activity' + str(j)
                for k in range(n_trl[0],n_trl[1]+1):
                    trl = 'Trial' + str(k)
                    subloc = sub+'\\'+act+'\\'
                    path1 = loc1+subloc + trl + '\\' + sub+act+trl+'.csv'
                    path2 = loc2 + subloc  + trl + '\\' 
                    features(path1,path2,sub,act,trl,j,twnd)
                    print(sub+act+trl+twnd+'DONE')

def main():
    d_base_path = ''
    features_path = ''
    extraction (d_base_path,features_path)
if __name__ == "__main__":
    main()
