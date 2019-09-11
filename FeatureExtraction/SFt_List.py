# -*- coding: utf-8 -*-
"""
Created on Thu Sep  5 18:16:36 2019

@author: 0169723
"""

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