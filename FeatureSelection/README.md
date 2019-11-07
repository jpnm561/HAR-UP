# Feature Selection

Here, you'll find a description of the feature selection process carried out by us.

## Pre-selection process

### What we used to do (Weka)

To begin selecting features, [Weka](https://www.cs.waikato.ac.nz/~ml/weka/index.html) was used, for attribute selection using Explorer mode and 10 folds for the selection, with the following models:

- CfsSubsetEval_BestFirst (with ZeroR set as the classifier)
					
- SubSetEval_Greedysepwise (with ZeroR set as the classifier)
					
- CorrelationAttributeEval_Ranker (with ZeroR set as the classifier)
					
- ClassifierAttributeEval_Ranker (with DecisionTable set as the classifier)
     
### Python alternative (FeaturePreSelection.py)

After our training experiments were done, we realised that since the use of Weka could be time consuming, changing the feature selection process entirely to Python would make our future work more efficient. Because of this **FeaturePreSelection.py** was made (although it was not used in our experiments). Currently, this program uses the following methods:

- Extra Trees Classifier (with 250 estimators and no random state).

- Linear SVC model with L2 as penalty.

- Recursive Feature Elimination with Random Forest as the classifier.

This program ranks features with these methods, then an array (containing 100 features, or 30% of all features if there are less than a hundred) is returned. These arrays are then compared and a report with the selected features is made, showing all of the selected features and the frequency that they appeared. If the frequency of a given feature is equal or bigger than 2, this feature is then considered important and chosen for the pre-selected features, outputting a new csv file with this selection.

To use this program, you'll simply have to run the function **preSelection()**, stating the *concepts* that are being used.

#### Directory arrangement

The following directory arrangement is necessary to run properly this program:

```
    FeaturePreSelection.py
    createFolder.py
    progressBar.py
    CONCEPT\
           \TIMEWINDOW\
	              \CONCPET_TIMEWINDOW.csv
```

After running the program, these will be the new files in the directory:


```
    CONCEPT\
           \TIMEWINDOW\
		      \PreSelection.csv
	              \PreSelectedFTS_TIMEWINDOW_CONCEPT.csv
```

#### Concept

A **concept** (or concepts) must be specified to begin running this program. To do so, just enter in the **concept** parameter in **preSelection()** which experiments you want to use for pre-selection. 


#### Time windows

Pre-selection is done by default for these time windows:

- 1&0.5

- 2&1

- 3&1.5

However, they can be altered when calling **preSelection()**, by modifying the **t_window** parameter. See the example below (under *Selection* or the repository's [README](https://github.com/jpnm561/HAR-UP/blob/master/README.md) for more information on this subject.


## RandomForest_Selection.py


This program takes the pre-selected features csv file and trains a random forest model with all features. After training, the model is fed features (adding one each time) and evaluates the results. A plot of the resulting scores (as well as these in a csv file) is produced. Using the plots, one can decide how many of the pre-selected features are relevant to the process.

### Direcotory arrangement

This program works by reading the pre-selected features file. This csv file only contains features and their respective tag (the Subject, Activity and Trial columns are missing in this file). These programs were made with the assumption that several experiments (the _concept_) will be performed, and therfore works with the following directory configuration:

```
    CONCEPT\
           \TIMEWINDOW\
	              \PreSelectedFTS_TIMEWINDOW_CONCEPT.csv
	              \PreSelectionReport_TIMEWINDOW_CONCEPT.csv
		      \PreSelectionReport_TIMEWINDOW_CONCEPT.png
	              \PreSel_RF_outputs\
		                        \Output1.csv
				        \Output2.csv
				        ...
					\OutputN.csv 
```


### Time windows

Selection is done for the selected time windows. By default these are:

- 1&0.5

- 2&1

- 3&1.5

These time windows can be altered when calling **sel_RF()** and **sel_Scores()**, by modifying the **t_window** parameter. See the example below or the repository's [README](https://github.com/jpnm561/HAR-UP/blob/master/README.md) for more information on this subject.

### Classification type

By default, scores are calculated assuming the use of a binary classification. This can be changed by altering the **binary** boolean variable in **sel_Scores()**

So calling:

```
    sel_Scores(concept,binary=False)
```   
   
 would get the scores for a multiclass classification.

## Example

The following example shows how to call the function for two windows: 1 second window, taken every 0.5 seconds; and 2 second window taken every second. This example uses a non-binary classification data set and two experiments: selected IMU features ('IMU') and selected Right-Pocket IMU features ('IMU-RightPocket').

```
    def main():
        concept = ['IMU','IMU-RightPocket']
        sel_RF(concept, t_window=['1&0.5','2&1'])
        sel_Scores(concept, t_window=['1&0.5','2&1'], binary=False)
    if __name__ == "__main__":
        main()
```

It is important to note that to run this successfully you'll need the following files:

```
    ParentFolder\
                \createFolder.py
                \RandomForest_Selection.py
                \IMU\
                    \1&0.5\
                          \PreSelectedFTS_1&0.5_IMU.csv
                    \2&1\
                        \PreSelectedFTS_2&1_IMU.csv
                \IMU-RightPocket\
                                \1&0.5\
                                      \PreSelectedFTS_1&0.5_IMU-RightPocket.csv
                                \2&1\
                                    \PreSelectedFTS_2&1_IMU-RightPocket.csv
```

After running the program, the new files in the directory will be:

```
    ParentFolder\
                \IMU\
                    \1&0.5\
                          \PreSelectionReport_1&0.5_IMU.csv
		          \PreSelectionReport_1&0.5_IMU.png
	                  \PreSel_RF_outputs\
		                            \Output1.csv
				            \Output2.csv
				            ...
				       	    \OutputN.csv
                    \2&1\
                        \PreSelectionReport_2&1_IMU.csv
		        \PreSelectionReport_2&1_IMU.png
	                \PreSel_RF_outputs\
		                          \Output1.csv
				          \Output2.csv
				          ...
				       	  \OutputN.csv
                \IMU-RightPocket\
                                \1&0.5\
                                      \PreSelectionReport_1&0.5_IMU-RightPocket.csv
		                      \PreSelectionReport_1&0.5_IMU-RightPocket.png
	                              \PreSel_RF_outputs\
		                                        \Output1.csv
				                        \Output2.csv
				                        ...
				       	                \OutputN.csv
                                \2&1\
                                    \PreSelectionReport_2&1_IMU-RightPocket.csv
		                    \PreSelectionReport_2&1_IMU-RightPocket.png
                                    \PreSel_RF_outputs\
		                                      \Output1.csv
				                      \Output2.csv
				                      ...
				       	              \OutputN.csv
```
