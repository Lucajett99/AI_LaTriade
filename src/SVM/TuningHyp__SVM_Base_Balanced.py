# -*- coding: utf-8 -*-
"""TuningHyperparameters _SVM_Base_balanced.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1_TuCwrKarcUGVx7a_zf7YJYx3VRn5vLG
"""

import pandas as pd
import numpy as np

#Read dataset
features =  pd.read_excel("../../dropoutData/Coorti 2016-2018 estrazione 2020 02 21 per AI.xlsx")

"""Rimpiazziamo i codici relativi a determinate feature con i nomi delle feature, così da poter utilizzare la funzione get_dummies() ed ottenere un one-hot-encoding"""

features["Diploma_scuola_superiore"] = features["Diploma_scuola_superiore"].map({1: "Classico", 2: "Scientifico", 3: "Linguistico", 4: "Magistrale", 5: "Artistico", 6: "Tecnico", 7: "Professionale", 8: "Altro_italiano", 9: "Estero", 99: "Non_disponibile"})
features["area_geografica_scuolasuperiore"] = features["area_geografica_scuolasuperiore"].map({1: "Emilia_romagna", 2: "Nord", 3: "Centro", 4: "Sud_isole", 5: "Estero", 99: "Non_disponibile"})
features["area_geografica_residenza"] = features["area_geografica_residenza"].map({1: "Emilia_romagna", 2: "Nord", 3: "Centro", 4: "Sud_isole", 5: "Estero", 99: "Non_disponibile"})
features["Ambito"] = features["Ambito"].map({1: "Economia", 2: "Farmacia", 3: "Giurisprudenza", 4: "Ingegneria", 5: "Lingue", 6: "Medicina", 7: "Veterinaria", 8: "Psicologia", 9: "Scienze", 10: "Scienze_agroalimanetari", 11: "Scienze_educazione_formazione", 12: "Scienze_motorie", 13: "Scienze_politiche", 14: "Scienze_statistiche", 15: "Sociologia", 16: "Studi_umanistici"})
features = pd.get_dummies(features)

"""Create and add age in DataFrame"""

from datetime import datetime, date

def getAge(dataNascita, coorte):
    ts = pd.to_datetime(str(dataNascita)) 
    born = ts.strftime('%d/%m/%Y')
    born = datetime.strptime(born, "%d/%m/%Y").date()
    date = "31/12/"+str(coorte)
    dataAttuale = datetime.strptime(date, "%d/%m/%Y").date()
    age = dataAttuale.year - born.year - ((dataAttuale.month, dataAttuale.day) < (born.month, born.day))
    return age

#add new column with NaN
features["Eta"] = np.nan

for ind in features.index:
    studente = features.iloc[ind]
    dataNascita = studente["DataNascita"]
    coorte = studente["Coorte"]
    #fill the new column with age 
    features.at[ind,'Eta'] = getAge(dataNascita, coorte)

print(features)

"""Abbiamo sostituito i valori NaN della feature "voto_scuola_superiore" con la media. Inoltre sono state droppate le colonne non utili ai fini dell'addestramento, ed infine eliminate le tuple contente almeno un NaN"""

mean_value = features['voto_scuola_superiore'].mean()
features['voto_scuola_superiore'] = features['voto_scuola_superiore'].fillna(mean_value)
features = features.drop('ID_Studente', axis = 1)
features = features.drop('Classe_ISEE', axis = 1)
features = features.drop('DataNascita', axis = 1)
features = features.drop('Coorte', axis = 1)
features = features.dropna()

"""Abbiamo bilanciato il dataset con approccio undersampling pareggiando il numero di dropout e non droput"""

#BILANCIAMENTO 1
"""
#Data preprocessing
dropout = pd.DataFrame()
noDropout = pd.DataFrame()

for ind in features.index:
    studente = pd.DataFrame(features.loc[[ind]])
    if features["Abbandoni"][ind] == 1:
        dropout = pd.concat([studente, dropout], ignore_index=True, axis = 0)
    else:
        noDropout = pd.concat([studente, noDropout], ignore_index=True, axis = 0)

#Bilanciamento dataset
final = pd.DataFrame()
for ind in dropout.index:
    studente_drop = pd.DataFrame(dropout.loc[[ind]])
    studente_noDrop = pd.DataFrame(noDropout.loc[[ind]])
    final = pd.concat([studente_drop, final], ignore_index=True, axis = 0)
    final = pd.concat([studente_noDrop, final], ignore_index=True, axis = 0)

features = final
print(len(features))
"""

"""La seguente cella serve a prescindere dal tipo di bilanciamento """

#Dividing the data into attributes and labels
X = features.drop('Abbandoni', axis=1)
y = features['Abbandoni']

#BILANCIAMENTO 2
from collections import Counter
from sklearn.datasets import make_classification
from imblearn.under_sampling import RandomUnderSampler

#Resampling data
rus = RandomUnderSampler(sampling_strategy = "majority", random_state=42)
X_res, y_res = rus.fit_resample(X, y)
print('Resampled dataset shape %s' % Counter(y_res))

X = X_res
y = y_res

from sklearn.model_selection import train_test_split as tts
#Dividing data into training and test sets
X_train, X_test, y_train, y_test = tts(X, y, test_size = 0.20, random_state=42)

"""Definition of a generalized training and test classification"""

from sklearn import metrics

def evaluate(model, test_features, test_labels):
    predictions = model.predict(test_features)
    tn, fp, fn, tp = metrics.confusion_matrix(test_labels, predictions).ravel()
    accuracy = metrics.accuracy_score(test_labels, predictions)
    classification_report = metrics.classification_report(test_labels, predictions)
    print("Model Performance:")
    print("true negative: ", tn)
    print("false negative: ", fn)
    print("true positive: ", tp)
    print("false positive: ", fp)
    print("Classification report:\n", classification_report)
    print("Accuracy:", accuracy)
    return accuracy

"""Create and fit random svm model with RandomizedSearchCV"""

from sklearn import svm
from sklearn.model_selection import RandomizedSearchCV, GridSearchCV

# defining parameter range 
param_grid = {'C': np.logspace(-3, 2, 6), 'kernel': ['linear']}  
svm_estimator = svm.SVC()
grid = GridSearchCV(svm_estimator, param_grid, refit = True, verbose = 3, n_jobs=-1) 
   
# fitting the model for grid search 
grid.fit(X_train, y_train)

# print and save best parameter and best estimator after tuning 
best_params = grid.best_params_
best_estimator = grid.best_estimator_
print(best_params)
print(best_estimator)

 
"""
# defining parameter range
random_grid = {'C': np.logspace(-5, 2, 6), 'kernel': ['linear']}
# First create the base model to tune
svm_estimator = svm.SVC()
# Random search of parameters, using 3 fold cross validation, 
# search across 3 different combinations, and use all available cores
svm_random = RandomizedSearchCV(estimator = svm_estimator, param_distributions = random_grid, n_iter = 5, cv = 3, verbose=2, random_state=42, n_jobs = -1)
# Fit the random search model
svm_random.fit(X_train, y_train)
#we save the best random estimator which will be used later for evaluation
best_random = svm_random.best_estimator_
"""

"""Print best values"""

"""
print("\n The best estimator across ALL searched params:\n", best_random)
print("\n The best score across ALL searched params:\n", svm_random.best_score_)
print("\n The best parameters across ALL searched params:\n", svm_random.best_params_)
"""

"""Create and print results of base model and random model

"""

base_model = svm.SVC(kernel='linear')
base_model.fit(X_train, y_train)
base_accuracy = evaluate(base_model, X_test, y_test)

random_accuracy = evaluate(best_estimator, X_test, y_test)
print('Improvement of {:0.2f}%.'.format( 100 * (random_accuracy - base_accuracy) / base_accuracy))