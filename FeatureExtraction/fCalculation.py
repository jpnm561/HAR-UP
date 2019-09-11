# -*- coding: utf-8 -*-
"""
Created on Tue Jul 31 11:44:19 2018
@author: José Pablo
"""

import numpy as np
from scipy.stats import kurtosis, skew, entropy
import pytest
from scipy.fftpack import rfft, rfftfreq
from datetime import datetime as dt


#using time as domain
def tdom(inpt,ftList):
    output = [] #the array we'll be returning:
    #[mean,standardDeviation,rootMeanSquare,maxAmp,minAmp,median,numZero-cross,
    #skewness,kurtosis,Q1,Q3,autocorrelation]
    rms = 0 #root mean square
    amp = [abs(inpt[i]) for i in range(0,len(inpt))] #to store amplitudes
    #variables used to count when zero is crossed
    bn = 1
    nzc = 0
    bnd = False
    bnF = False
    for i in range(0, len(inpt)):
        rms = rms + (inpt[i]**2)
        #this is to see when zero is being crossed:
        if (inpt[i] != 0):
            bnd = True
            if(bnF == False):
                bnF = True
                bn = inpt[i]/abs(inpt[i])
        else:
            bnd = False
        if (bnd):
            sgn = inpt[i]/abs(inpt[i])
            if (sgn != bn):
                nzc = nzc + 1
            bn = inpt[i]/abs(inpt[i])
    for feature in ftList:
        if feature == 'Mean':
            output.append(np.mean(inpt))
        elif feature == 'StandardDeviation':
            output.append(np.std(inpt))
        elif feature == 'RootMeanSquare':
            output.append((np.sqrt(rms) / np.sqrt(len(inpt))))
        elif feature == 'MaximalAmplitude':
            output.append(max(amp))
        elif feature == 'MinimalAmplitude':
            output.append(min(amp))
        elif feature == 'Median':
            output.append(np.median(inpt))
        elif feature == 'Number of zero-crossing':
            output.append(nzc)
        elif feature == 'Skewness':
            output.append(skew(inpt))
        elif feature == 'Kurtosis':
            output.append(kurtosis(inpt))
        elif feature == 'First Quartile':
            output.append(np.percentile(inpt,25,interpolation = 'midpoint'))
        elif feature == 'Third Quartile':
            output.append(np.percentile(inpt,75,interpolation = 'midpoint'))
        elif feature == 'Autocorrelation':
            kt = np.correlate(inpt,inpt,mode='full')
            output.append(np.median(kt))
    return output
#end tdom

#using frequency as domain
def fdom(values, timestamps, ftList):
    output = []
    fdarr = abs(rfft(values))#real absolute FFT of 'values'
    for feature in ftList:
        if feature == 'Energy':
            output.append(np.sum(fdarr**2)) 
    return output
#end fdom

#a function to obtain the average frequency form the timestamps
def avfreq(inpt):
    tst = [inpt[i].split('T') for i in range(0,len(inpt))]
    frmt = '%H:%M:%S.%f'
    x = [dt.strptime(tst[i][1][:-3], frmt) for i in range(0,len(tst))]
    dif = [(x[i+1] - x[i]).microseconds for i in range(0, len(x)-1)]
    return (1000000 / np.mean(dif))
#end avfreq