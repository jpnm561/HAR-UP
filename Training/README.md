# Training

Both _Training_ files train, validate and get scores (accuracy, precision, recall and f1-score) for said validation. To train, 70% of the available data is randomly selected (for binary classifications 70% of fall data and 70% of other data are selected), leaving the remaining 30% for validation.


All of the resulting validation data sets are stored, as well as scores (in csv files), confusion matrix and bar graphs (as jpg files) for all scores.

## Directory arrangement

This program works by reading the selected features file. This is a csv file containign only the desired features for training (the Subject, Activity, Trial and Tag columns are missing in this file). These programs were made with the assumption that several experiments (the _concept_) will be performed, and therfore work with the following directory configuration:


- Direcory before running the program:

```
    CONCEPT\
           \TIMEWINDOW\
                      \SelectedFeatures_TIMEWINDOW_CONCEPT.csv
```

- Directory after running the program:

```
    CONCEPT\
           \AvgConfusionMatrix_METHOD_CONCEPT.jpg
           \Score_Mean_CONCEPT.jpg
           \Score_StandardDeviation_CONCEPT.jpg
           \Score_CONCEPT_temp.csv
           \TIMEWINDOW\
                      \SelectedFeatures_TIMEWINDOW_CONCEPT.csv
                      \METHOD\
                             \Result_TIMEWINDOW_METHOD_1.csv
                             \Result_TIMEWINDOW_METHOD_2.csv
                             ...
                             \Result_TIMEWINDOW_METHOD_10.csv
                             \AvgConfusionMatrix_TIMEWINDOW_METHOD_CONCEPT.jpg
                             \Score_TIMEWINDOW_METHOD_CONCEPT.csv 
```

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

## Classification type

This program can work with either binary classifications or multiclass classifications. To work with binary classifications, you should use **BC_Training()** and **BC_Scores()**, and if you want to work with a multiclass classification **MC_Training()** and **MC_Scores()** should be selected.

## Example

The following example shows how to call the function to train using only Random Forest for two windows: 1 second window, taken every 0.5 seconds; and 2 second window taken every second. This example uses a binary classification data set and two experiments: selected IMU features ('IMU') and selected Right-Pocket IMU features ('IMU-RightPocket').

    def main():
        concept = ['IMU','IMU-RightPocket']
        BC_Training(concept, t_window=['1&0.5','2&1'], methods=['RF'])
        BC_Scores(concept, t_window=['1&0.5','2&1'], methods=['RF'])
    if __name__ == "__main__":
        main()


It is important to note that to run this successfully you'll need the following files:


    ParentFolder\
                \BC_Training.py
                \createFolder.py
                \scorePlots.py
                \IMU\
                    \1&0.5\
                          \SelectedFeatures_1&0.5_IMU.csv
                    \2&1\
                        \SelectedFeatures_2&1_IMU.csv   
                \IMU-RightPocket\
                                \1&0.5\
                                      \SelectedFeatures_1&0.5_IMU-RightPocket.csv
                                \2&1\
                                    \SelectedFeatures_2&1_IMU-RightPocket.csv


After running the program, the new files in the directory will be:


    ParentFolder\
                \IMU\
                    \AvgConfusionMatrix_RF_IMU.jpg
                    \Score_Mean_IMU.jpg
                    \Score_StandardDeviation_IMU.jpg
                    \Score_IMU_temp.csv
                    \1&0.5\
                          \AvgConfusionMatrix_1&0.5_RF_IMU.jpg
                          \Score_1&0.5_RF_IMU.csv
                          \RF\
                             \Result_1&0.5_RF_1.csv
                             \Result_1&0.5_RF_2.csv
                             ...
                             \Result_1&0.5_RF_10.csv
                    \2&1\
                        \AvgConfusionMatrix_2&1_RF_IMU.jpg
                        \Score_2&1_RF_IMU.csv
                        \RF\
                           \Result_2&1_RF_1.csv
                           ...
                           \Result_2&1_RF_10.csv
                \IMU-RightPocket\
                                \AvgConfusionMatrix_RF_IMU-RightPocket.jpg
                                \Score_Mean_IMU-RightPocket.jpg
                                \Score_StandardDeviation_IMU-RightPocket.jpg
                                \Score_IMU-RightPocket_temp.csv
                                \1&0.5\
                                      \AvgConfusionMatrix_1&0.5_RF_IMU-RightPocket.jpg
                                      \Score_1&0.5_RF_IMU-RightPocket.csv
                                      \RF\
                                         \Result_1&0.5_RF_1.csv
                                         ...
                                         \Result_1&0.5_RF_10.csv
                                \2&1\
                                    \AvgConfusionMatrix_2&1_RF_IMU-RightPocket.jpg
                                    \Score_2&1_RF_IMU-RightPocket.csv
                                    \RF\
                                       \Result_2&1_RF_1.csv
                                       ...
                                       \Result_2&1_RF_10.csv
