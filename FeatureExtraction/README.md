# FeatureExtraction.py

## Directory arrangement

The feature extraction program works by reading hte desired subject and activity trial files. This means that the program reads individual trial files and not the complete data set file. The directory arrangement is the following:


    ParentFolder\Subject#\Activity#\Trial#\Subject#Activity#Trial#.csv


If the default path to store the features is used, they will be stored in the same folder as the trial data files, and a single file (containign all features for a specified time window) will be created in the parent folder (where the Subject folders are stored).


    ParentFolder\FeaturesTIMEWINDOW.csv
                \Subject#\Activity#\Trial#\Subject#Activity#Trial#.csv
                                          \Subject#Activity#Trial#FeaturesTIMEWINDOW.csv


## Choosing a time window

By default, features are calculated for three time windows:

- 1&0.5

- 2&1

- 3&1.5

These time windows can be altered when calling the function **extraction()**

### Choosing different header formats

We have two available header formats:

1.

  ![](header1.png)
  
  
  To get this header the **extraction** function should just be called as usual:
  
  
    extraction(d_base_path,features_path)


2. 

  ![](header2.png)


  This header requires a flag to specify that timestamps are wanted. To get it, the **extraction** function should be called as:
  
  
    extraction(d_base_path,features_path, t_stamp = True)


## Choosing sensors and features

By default, the program gets the features for 42 "sensors":

- 5 IMU sensors, each one with:

  - 3 Accelerometer (x, y and z axis)

  - 3 Angular Velocity (x, y and z axis)

  - Luminosity

- 6 Infrared sensors

- 1 Think-gear sensor

There are 13 default features obtained are:

- Mean

- StandardDeviation

- RootMeanSquare

- MaximalAmplitude

- MinimalAmplitude

- Median

- Number of zero-crossing

- Skewness

- Kurtosis

- First Quartile

- Third Quartile

- Autocorrelation

- Energy


These sensors and features are all listed in **SFt_List.py**, and altering said file will allow you to choose which sensors and features to use. All feature calculations can be found in **fCalculation.py**.
