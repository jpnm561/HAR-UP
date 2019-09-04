# HAR-UP
## Multimodal System for Fall Detection

In this repository you'll be able to find the python programs used for the Universidad Panamericana's Multimodal System for Fall Detection.
 These are all written  in python.
 
We have the programs for feature selection, training and validation. Features were calculated using three different time-windows: 1&0.5, 2&1 and 3&1.5. For each time-window, the first number refers to the separation (in seconds) in which the features were obtained, while the second number refers to the window-lenght (also in seconds) each feature considered.

## How to use the programs

The available programs were used in the following manner and order:

1. First of all, the desired features were placed in a csv file.

2. A (preliminar) feature selection process was made. To select the features, Weka *add citation* was used, with attribute selection using Explorer mode and 10 folds for the selection, with the following models:

					-CfsSubsetEval_BestFirst (with ZeroR set as the classifier)
					
					-SubSetEval_Greedysepwise (with ZeroR set as the classifier)
					
					-CorrelationAttributeEval_Ranker (with ZeroR set as the classifier)
					
					-ClassifierAttributeEval_Ranker (with DecisionTable set as the classifier)
     
3. After the first feature selection was completed, the selected features were written in a new csv file.

4. Having the new csv file, the selected features were placed in a second selection process. This time Random Forest was used, to train a model with the all the selected features. After training, features were added (one at a time) to see which features were the most relevant.

5. The results were then evaluated, and their scores were analyzed to finish the second selection process.

6. Using the selected features (from the second selection process), the real training could be started. This was done by training the four different models (RF, SVM, KNN, MLP) with random data. 70% of the data base was used for training, leaving the remaining 30% for validation. This was done ten times for all the modles (ten training and validation sets were made for the four models, for each one of the time windows). 

7. After validation was completed, scores were obtained for said validation.

## Citation

**If you use the data set (https://sites.google.com/up.edu.mx/har-up/p%C3%A1gina-principal), please cite as follows:**

*Lourdes Martínez-Villaseñor, Hiram Ponce, Jorge Brieva, Ernesto Moya-Albor, José Núñez-Martínez, Carlos Peñafort-Asturiano, “UP-Fall Detection Dataset: A Multimodal Approach”, Sensors 19(9), 1988: 2019, doi:10.3390/s19091988.*
