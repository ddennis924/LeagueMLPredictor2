
from tkinter import Y
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import xgboost as xgb
from sklearn.compose import ColumnTransformer, make_column_transformer
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    f1_score,
    make_scorer,
    ConfusionMatrixDisplay,
)
from sklearn.model_selection import (
    GridSearchCV,
    RandomizedSearchCV,
    cross_val_score,
    cross_validate,
    train_test_split,
)
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, StandardScaler
from sklearn.svm import SVC
from xgboost import XGBClassifier
from sklearn.ensemble import VotingClassifier

def mean_std_cross_val_scores(model, X_train, y_train, **kwargs):
    """
    Returns mean and std of cross validation

    Parameters
    ----------
    model :
        scikit-learn model
    X_train : numpy array or pandas DataFrame
        X in the training data
    y_train :
        y in the training data

    Returns
    ----------
        pandas Series with mean scores from cross_validation
    """

    scores = cross_validate(model, X_train, y_train, **kwargs)

    mean_scores = pd.DataFrame(scores).mean()
    std_scores = pd.DataFrame(scores).std()
    out_col = []

    for i in range(len(mean_scores)):
        out_col.append((f"%0.5f (+/- %0.5f)" % (mean_scores[i], std_scores[i])))

    return pd.Series(data=out_col, index=mean_scores.index)

# pd1 = pd.read_csv("LeagueMatches.csv", index_col=0)
# pd2 = pd.read_csv("LeagueMatches2.csv", index_col=0)
# pd3 = pd.read_csv("LeagueMatches3.csv", index_col=0)
# pds = [pd1, pd2, pd3]
# temp = pd.concat(pds)

df = pd.read_csv("LeagueMatches4.csv", index_col=0)
df = df.replace(-1, np.nan)
df = df.dropna()

train_df, test_df = train_test_split(df, test_size=0.2)

X_train = train_df.drop(columns='winner')
y_train = train_df['winner']
X_test = test_df.drop(columns='winner')
y_test = test_df['winner']
cat_feats = ['blueTops', 'blueJngs', 'blueMids', 'blueBots', 'blueSups', 'redTops', 'redJngs', 'redMids', 'redBots', 'redSups']
num_feats = ['btmp', 'btlevel', 'btct', 'btt', 'bjmp', 'bjlevel', 'bjct', 'bjt', 'bmmp', 'bmlevel', 'bmct', 'bmt', 'bbmp', 'bblevel', 'bbct', 'bbt', 'bsmp', 'bslevel', 'bsct', 'bst',]
pass_feats = ['btwr', 'btcwr', 'btkda', 'bjwr', 'bjcwr', 'bjkda', 'bmwr', 'bmcwr', 'bmkda','bbwr', 'bbcwr', 'bbkda', 'bswr', 'bscwr', 'bskda']

preprocessor = make_column_transformer((OneHotEncoder(handle_unknown='ignore'), cat_feats), 
(make_pipeline(SimpleImputer(),StandardScaler()), num_feats),
(SimpleImputer(), pass_feats))

dummy = make_pipeline(preprocessor, DummyClassifier())
cross_val_results_dummy = pd.DataFrame(
    cross_validate(dummy, X_train, y_train, return_train_score=True)
)
print(cross_val_results_dummy.head())

from xgboost import XGBClassifier

# models = {
#     "SVC": make_pipeline(preprocessor, SVC()),
#     "Random Forest": make_pipeline(preprocessor, RandomForestClassifier()),
#     "XGB": make_pipeline(
#     preprocessor, XGBClassifier( eval_metric="logloss", verbosity=0,use_label_encoder=False)),
# }

# # imported from lecutre 11
# results = {}
# for (name, model) in models.items():
#     results[name] = mean_std_cross_val_scores(
#         model, X_train, y_train, return_train_score=True
#     )
# print(pd.DataFrame(results).T)

# param_grid = {
#     "svc__class_weight": ['balanced', None],
#     "svc__gamma": [0.0005, 0.001, 0.01, 0.1, 1.0 ,10],
#     "svc__C":[0.001, 0.01, 0.1, 1.0, 10, 100]
# }
# pipe_svc = make_pipeline(preprocessor, SVC())
# rand_search = GridSearchCV(pipe_svc, param_grid=param_grid, n_jobs=-1, cv=10)


# rand_search.fit(X_train, y_train)
# print("best params for accuracy:")
# print(rand_search.best_params_)
# print("best score for accuracy:")
# print(rand_search.best_score_)
pipe_svc = make_pipeline(preprocessor, SVC(C=100, gamma=0.001,probability=True))
cross_val_results_svc = pd.DataFrame(
    cross_validate(pipe_svc, X_train, y_train, return_train_score=True)
)
print("svc")
print(cross_val_results_svc.to_string())
pipe_svc.fit(X_train, y_train)
print(pipe_svc.score(X_test, y_test))

# param_grid = {"xgbclassifier__learning_rate": [0, 0.1, 0.25, 0.4, 0.75],
#               "xgbclassifier__n_estimators":[20, 50, 100, 200, 300,400],
#               "xgbclassifier__max_depth":[1,2,3,4,5]
#               }
# pipe_xgb = make_pipeline(preprocessor, XGBClassifier(eval_metric='logloss', verbosity=0))
# rand_search_xgb = GridSearchCV(pipe_xgb, param_grid=param_grid, n_jobs=-1, cv=10)


# rand_search_xgb.fit(X_train, y_train)
# print("best params for accuracy:")
# print(rand_search_xgb.best_params_)
# print("best score for accuracy:")
# print(rand_search_xgb.best_score_)

pipe_xgb = make_pipeline(preprocessor, XGBClassifier(eval_metric='logloss', verbosity=0, learning_rate=0.25,n_estimators=100,max_depth=2))
cross_val_results_xgb = pd.DataFrame(
    cross_validate(pipe_xgb, X_train, y_train, return_train_score=True)
)
print("xgb")
print(cross_val_results_xgb.to_string())
pipe_xgb.fit(X_train, y_train)
print(pipe_xgb.score(X_test, y_test))

# param_grid = {"randomforestclassifier__max_depth": [1, 10, 20, 50, 70, 100],
#               "randomforestclassifier__n_estimators":[1, 10, 20, 50, 100, 200, 300], 
#               "randomforestclassifier__max_features":[1, 10, 20, 20, 40, 50]}
# pipe_rf = make_pipeline(preprocessor, RandomForestClassifier())
# rand_search_rf = GridSearchCV(pipe_rf, param_grid=param_grid, n_jobs=-1, cv=10)


# rand_search_rf.fit(X_train, y_train)
# print("best params for accuracy:")
# print(rand_search_rf.best_params_)
# print("best score for accuracy:")
# print(rand_search_rf.best_score_)

pipe_rf = make_pipeline(preprocessor, RandomForestClassifier(max_depth=50, max_features=50, n_estimators=300))
cross_val_results_rf = pd.DataFrame(
    cross_validate(pipe_rf, X_train, y_train, return_train_score=True)
)
print("rf")
print(cross_val_results_rf.to_string())
pipe_rf.fit(X_train, y_train)
print(pipe_rf.score(X_test, y_test))


# pipe_lr = make_pipeline(preprocessor, LogisticRegression(max_iter=1000))
# param_grid = {
#     "logisticregression__C":[0.00001, 0.0001, 0.001, 0.01, 0.1, 1.0],
#     "logisticregression__solver": ['liblinear', 'lbfgs']
# }
# rand_search_lr = GridSearchCV(pipe_lr, param_grid=param_grid, n_jobs=-1, cv=10)

# rand_search_lr.fit(X_train, y_train)
# print("best params for accuracy:")
# print(rand_search_lr.best_params_)
# print("best score for accuracy:")
# print(rand_search_lr.best_score_)
pipe_lr = make_pipeline(preprocessor, LogisticRegression(C=1.0, max_iter=10000))
cross_val_results_lr = pd.DataFrame(
    cross_validate(pipe_lr, X_train, y_train, return_train_score=True)
)
print("lr")
print(cross_val_results_lr.to_string())
pipe_lr.fit(X_train, y_train)
print(pipe_lr.score(X_test, y_test))

classifier = {"rf": pipe_rf, 'xgb': pipe_xgb}
average_model = VotingClassifier(list(classifier.items()), voting='soft')
cross_val_results_avg = pd.DataFrame(
    cross_validate(average_model, X_train, y_train, return_train_score=True)
)
print(cross_val_results_avg.to_string())
average_model.fit(X_train, y_train)
print(average_model.score(X_test, y_test))

from sklearn.ensemble import StackingClassifier
estimators = [('rf', RandomForestClassifier(max_depth=50, max_features=50, n_estimators=300)), 
('xgb',XGBClassifier(eval_metric='logloss', verbosity=0, learning_rate=0.25,n_estimators=100,max_depth=2))]
clf = make_pipeline(preprocessor, StackingClassifier(estimators=estimators))
clf.fit(X_train, y_train)
print(clf.score(X_test, y_test))
import pickle

pipe_xgb.fit(df.drop(columns='winner'), df['winner'])
filename = 'finalized_model.sav'
pickle.dump(pipe_xgb, open(filename, 'wb'))
