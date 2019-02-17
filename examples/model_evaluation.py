# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split, GridSearchCV, \
                                    cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

wine = load_wine()

X_train, X_test, \
y_train, y_test = train_test_split(wine.data, wine.target,
                                   stratify=wine.target, random_state=0)

def nested_cross_validation(estimator, param_grid, X_train, y_train):
    gs = GridSearchCV(estimator, param_grid, cv=2)
    s = cross_val_score(gs, X_train, y_train, cv=5)
    print('CV accuracy: %.4f +/- %.4f' % (np.mean(s), np.std(s)))

# Algorithm selection

print('\n*Logistic Regression*')
p = Pipeline([('pp1', StandardScaler()), 
              ('clf', LogisticRegression(random_state=0, 
                                         class_weight='balanced'))])
lr_grid = {'clf__C': [0.001, 0.1, 1, 10, 100]}
nested_cross_validation(p, lr_grid, 
                        X_train, y_train)

print('\n*SVC*')
p = Pipeline([('pp1', StandardScaler()), 
              ('clf', SVC(random_state=0, class_weight='balanced'))])
svc_grid = {'clf__C': [0.001, 0.1, 1, 10, 100], 
            'clf__gamma': [0.001, 0.1, 1, 10, 100, 'auto']}
nested_cross_validation(p, svc_grid, 
                        X_train, y_train)


# Model training
print('\n*Model Training*')
p = Pipeline([('pp1', StandardScaler()), 
              ('clf', SVC(random_state=0, class_weight='balanced'))])
svc_grid = {'clf__C': [0.001, 0.1, 1, 10, 100], 
            'clf__gamma': [0.001, 0.1, 1, 10, 100, 'auto']}
gs = GridSearchCV(p, svc_grid, cv=3)
gs.fit(X_train, y_train)
print('SVC best training score:', gs.best_score_)
print('SVC best params:', gs.best_params_)
model_params = gs.best_estimator_.named_steps['clf'].get_params()

# Performance evaluation
print('\n*Performance Evaluation*')
print('SVC test score:', gs.score(X_test, y_test))

# Final model
print('\n*Final Model*')
p = Pipeline([('pp1', StandardScaler()), 
              ('clf', SVC(**model_params))])
p.fit(wine.data, wine.target)
print('SVC params:', p.named_steps['clf'].get_params())
 