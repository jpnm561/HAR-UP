# Feature Selection

Here, you'll find a description of the feature selection process carried out by us.

## Pre-selection process

To begin selecting features, [Weka](https://www.cs.waikato.ac.nz/~ml/weka/index.html) was used, for attribute selection using Explorer mode and 10 folds for the selection, with the following models:

					-CfsSubsetEval_BestFirst (with ZeroR set as the classifier)
					
					-SubSetEval_Greedysepwise (with ZeroR set as the classifier)
					
					-CorrelationAttributeEval_Ranker (with ZeroR set as the classifier)
					
					-ClassifierAttributeEval_Ranker (with DecisionTable set as the classifier)
     

## RandomForest_Selection.py


This program takes the pre-selected features csv file and trains a randomm forest model with all features. After trainig, the model is fed the features (adding one each time) and evaluates the results. A plot of the resulting scroes (as well as these in a csv file) is produced. Using the plots, one can decide how many of the pre-selected features are relevant to the process.

### Direcotory arrangement



### Concept selection

It is necessary for the user to state the concept (or experiment) that is being performed. This refers to a

(concept,t_window=['1&0.5', '2&1', '3&1.5'],scr_dir=''):
