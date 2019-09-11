# Trainig

Both _Training_ files train, validate and get scores (accuracy, precision, recall and f1-score) for said validation. To train, 70% of the available data is randomly selected (for binary classifications 70% of fall data and 70% of other data are selected), leaving the remaining 30% for validation.


All of the resulting validation data sets are stored, as well as scores (in csv files), confusion matrix and bar graphs (as jpg files) for all scores.

## Directory arrangement

This program works by reading the selected features file. This is a csv file containign only the desired features for training (the Subject, Activity, Trial and Tag columns are missing in this file). These programs were made with the assumption that several experiments (the _concept_) will be performed, and therfore work with the following directory configuration:


    Concept\
           \AvgConfusionMatrix_Method_Concept.jpg
           \AvgConfusionMatrix_Method_Concept.jpg
           \Score_Mean_Concept.jpg
           \Score_StandardDeviation_Concept.jpg
           \Score_Concept_temp.csv
           \TimeWindow\SelectedFeatures_TimeWindow_Concept.csv
                      \Method\Result_TimeWindow_Method_ResultNumber.csv
                             \AvgConfusionMatrix_TimeWindow_Method_Concept.jpg
                             \Score_TimeWindow_Method_Concept.csv
    

## Methods

Training is done 10 times with different data sets, and by default is done with four methods:


- Random Forest (RF)

- Support Vector Machines (SVM)

- Multi-Layer Perceptron Neural Network (MLP)

- K-Nearest Neighbour (KNN)


If you don't need to work with all four methods, the desired methods can be selected in the function. 

## Time windows

Training is done for the selected time windows. By default these are:

- 1&0.5

- 2&1

- 3&1.5

These time windows can be altered when calling **BC/MC_Training()** and **BC/MC_Scores()**
