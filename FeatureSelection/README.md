# Feature Selection

Here, you'll find a description of the feature selection process carried out by us.

## RandomForest_Selection.py


This program takes the pre-selected features csv file and trains a randomm forest model with all features. After trainig, the model is fed the features (adding one each time) and evaluates the results. A plot of the resulting scroes (as well as these in a csv file) is produced. Using the plots, one can decide how many of the pre-selected features are relevant to the process.
