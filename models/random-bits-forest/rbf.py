## Applying ML algorithms to detect eye state

import numpy as np
import pandas as pd
import time

from sklearn.model_selection import cross_val_score, GridSearchCV, cross_validate, train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.svm import SVC
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, normalize
from sklearn.decomposition import PCA

######################################### Reading and Splitting the Data ###############################################
# Read in all the data.

# To run: python rbf.py

data = pd.read_csv('blinks-input.csv')

# Separate out the x_data and y_data.
x_data = data.loc[:, data.columns != "y"]
y_data = data.loc[:, "y"]

# The random state to use while splitting the data.
random_state = 100

# Split 70% of the data into training and 30% into test sets. Call them x_train, x_test, y_train and y_test.
# Use the train_test_split method in sklearn with the parameter 'shuffle' set to true and the 'random_state' set to 100.
x_train, x_test, y_train, y_test = train_test_split(x_data, y_data, test_size=0.3, shuffle='true', random_state=random_state)

# ##############################################Linear Regression ###################################################
# Create a LinearRegression classifier and train it.

# print("----------------------\ndata.describe()\n")
# data.describe()

# regressor = LinearRegression()  
# regressor.fit(x_train, y_train)

#coeff_df = pd.DataFrame(regressor.coef_, x_data.columns, columns=['Coefficient'])  
#print(coeff_df)
#print("Above: For a unit increase in column X1, the last column changes by -0.000878\r")

# Test its accuracy (on the training set) using the accuracy_score method.
# Test its accuracy (on the testing set) using the accuracy_score method.
# Note: Round the output values greater than or equal to 0.5 to 1 and those less than 0.5 to 0. You can use y_predict.round() or any other method.

# accuracy = regressor.score(x_test,y_test)
# print("Accuracy (regressor.score for x_test,y_test): " + str(accuracy))

# y_pred_train = regressor.predict(x_train)
# print("y_pred_train list: " + str(y_pred_train))

# y_pred = regressor.predict(x_test) # Resulting list is always the same
# print("y_pred list: " + str(y_pred))


#accuracy2 = accuracy_score(x_data, y_predict, normalize=False)
#print("Accuracy2 " + str(accuracy2))

#print("Accuracy Score: " + str(accuracy_score(y_test,y_pred, normalize=False)))
# Without round:
# Classification metrics can't handle a mix of binary and continuous targets
# https://stackoverflow.com/questions/38015181/accuracy-score-valueerror-cant-handle-mix-of-binary-and-continuous-target

# print("\nLR Accuracy Training accuracy_score(y_train, y_pred_train.round()...): " + str(accuracy_score(y_train, y_pred_train.round(), normalize=True)))

# print("LR Accuracy Testing accuracy_score(y_test, y_pred.round()...): " + str(accuracy_score(y_test, y_pred.round(), normalize=True)))
# Note: y_test is the same as y_true (the variable containing the class/labels that the algorithm is trying to predict.)
# Also note that normalize=False is omitted, otherwise 2873 returned

# print("LR Accuracy (regressor.score for x_data, y_data): " + str(regressor.score(x_data, y_data)))

# Right column is the angle of the line, hence it does not match 0 and 1 values in first column.
#df = pd.DataFrame({'LR Actual': y_test, 'Predicted LinearRegression': y_pred})  
#print(df)

#from sklearn import metrics
#print('LR Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_pred))  
#print('LR Mean Squared Error:', metrics.mean_squared_error(y_test, y_pred))  
#print('LR Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, y_pred))) 

# Reshape your data either using array.reshape(-1, 1) if your data has a single feature or array.reshape(1, -1) if it contains a single sample.
#print("Accuracy (regressor.score for y_test, y_pred.round()): " + str(regressor.score(y_test, y_pred.round))) 

#regressor.coef_ array([1., 2.])
#regressor.intercept_ 3.0000...
#regressor.predict(np.array([[3, 5]])) array([16.])

# print("----------------------")

# ############################################### Random Forest Classifier ##############################################
# Create a RandomForestClassifier and train it.


#Create a Gaussian Classifier
rf_classifier=RandomForestClassifier(n_estimators=10) # At 100 training accuracy is 1.0.  (14980 records.)
rf_classifier.fit(x_train,y_train)
y_pred_train = rf_classifier.predict(x_train)
y_pred=rf_classifier.predict(x_test)

# Test its accuracy on the training set using the accuracy_score method.
# Test its accuracy on the test set using the accuracy_score method.

# Model Accuracy, how often is the classifier correct?
# print("RandomForestClassifier Training Accuracy before tuning: ",accuracy_score(y_train, y_pred_train))
# print("RandomForestClassifier Test Set Accuracy before tuning: ",accuracy_score(y_test, y_pred))

#RandomForestClassifier Training Accuracy: 0.9964714857905779
#RandomForestClassifier Test Set Accuracy: 0.9023141967067201, also .89 (sometimes higher than 0.89 from RandomForestRegressor below)

# Determine the feature importance as evaluated by the Random Forest Classifier.
#       Sort them in the descending order and print the feature numbers. The report the most important and the least important feature.
#       Mention the features with the exact names, e.g. X11, X1, etc.
#       Hint: There is a direct function available in sklearn to achieve this. Also checkout argsort() function in Python.


importances = rf_classifier.feature_importances_
std = np.std([tree.feature_importances_ for tree in rf_classifier.estimators_],
             axis=0)
indices = np.argsort(importances)[::-1]

# Print the feature ranking
# print("\nRandom Forest Feature Importance:")

# Values change each time
# for f in range(x_data.shape[1]):
#     print("%d. X%d (%f)" % (f + 1, indices[f] + 1, importances[indices[f]]))

# Tune the hyper-parameters 'n_estimators' and 'max_depth'.
#       Print the best params, using .best_params_, and print the best score, using .best_score_.

param_grid = {
	'max_depth': [None,3,8],
    'n_estimators': [50, 100, 200, 1000]
}

# Using GridSearchCV 

# From Piaza: Use only the TRAINING DATASET for the GridSearch and then check the accuracy 
# of the best fit model parameters on the test data. TA Vatsal Srivastava provided this link:
# https://stackoverflow.com/questions/45394527/do-i-need-to-split-data-when-using-gridsearchcv/45394598#45394598
# 1) Take your original dataset and hold out some data as a test set (Say, 10%. We're using 30%)
# 2) Use grid search on remaining 90%. Split will be done for you by the algorithm here.
# 3) After you got optimal hyperparameters, test it on the test set from #1 to get final estimate of the performance you can expect on new data.
# I assume this already occured above.

# Question: Why is cv not returned by get_params() above?

rf_tune = GridSearchCV(rf_classifier, param_grid=param_grid, cv=10, n_jobs=-1) #  n_jobs=-1 runs on all processors

rf_tune.fit(x_train, y_train) # train_features and train_labels
### best_params_  {'n_estimators': 400, 'min_samples_split': 2, 'min_samples_leaf': 1, 'max_features': 'sqrt', 'max_depth': None, 'bootstrap': False}
# print ("\nbest_params_ " + str(rf_tune.best_params_))

# Random Forest - Testing Accuracy after tuning:
# print ("Random Forest - Testing Accuracy after tuning (best_score_) " + str(rf_tune.best_score_))

# print("\n----------------------------")

y_pred_train_rf = rf_tune.predict(x_train)
y_pred_test_rf = rf_tune.predict(x_test)
print("Random Forest - Training Accuracy after tuning:" + str(accuracy_score(y_train, y_pred_train_rf)))
print("Random Forest - Testing Accuracy after tuning:" + str(accuracy_score(y_test, y_pred_test_rf)))

# print("\nrf_tune.cv_results_")
# for key,val in rf_tune.cv_results_.items():
#    print (key, ":\n", val)

# feature importance after tuning
importances_tune = rf_tune.best_estimator_.feature_importances_
indices_tune = np.argsort(importances_tune)[::-1]

feature_ls = []
importance_ls = []
for f in range(x_data.shape[1]):
    feature_ls.append(f"X{indices_tune[f] + 1}")
    importance_ls.append(importances_tune[indices_tune[f]])

feature_ls.append("Random Forest - Training Accuracy after tuning:")
importance_ls.append(str(accuracy_score(y_train, y_pred_train_rf)))

feature_ls.append("Random Forest - Testing Accuracy after tuning:")
importance_ls.append(str(accuracy_score(y_test, y_pred_test_rf)))

out = pd.DataFrame(data={"feature":feature_ls,"level of importance":importance_ls})
out.to_csv("../../output/blinks/blinks-rbforest-output.csv",index=False)


# ############################################ Support Vector Machine ###################################################
# Pre-process the data to standardize or normalize it, otherwise the grid search will take much longer
# Create a SVC classifier and train it.

# print("----------------------")
# print('Support Vector Matching (SVM)')

# https://towardsdatascience.com/scale-standardize-or-normalize-with-scikit-learn-6ccc7d176a02
# Normalizer works on the rows, not the columns.

# StandardScaler and normalize were declared in skeleton

# https://scikit-learn.org/stable/modules/preprocessing.html
#from sklearn import preprocessing
#data_normalized = preprocessing.normalize(scaler.transform(data), norm='l2')

# StandardScaler(copy=True, with_mean=True, with_std=True)
# scaler = StandardScaler()

# "Test it on the test set to get final estimate of the performance you can expect on new data."
# x_test_normalized = normalize(scaler.fit_transform(x_test), norm='l2')
# x_train_normalized = normalize(scaler.fit_transform(x_train), norm='l2')

# Following from link provided in Piaza
# https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GridSearchCV.html

# start_time  = time.time() # datetime.datetime.now()
# svc = SVC(gamma="scale")

# parameters = {'kernel':('linear', 'rbf'), 'C':[.01, .1, 1]} # FASTER

# return_train_score needed for 'mean_train_score'
# grid_search = GridSearchCV(svc, parameters, cv=10, return_train_score=True, n_jobs=-1) #  n_jobs=-1 runs on all processors

# print("SVM parameters:")
# for key,val in parameters.items():
    # print (key, ": ", val)

# print("\nA processor timeout error may occur since n_jobs=-1 is used to run on all processors.\nOkay to ignore timeout / memory leak error.\n")
# Full error: UserWarning: A worker stopped while some jobs were given to the executor.
# This can be caused by a too short worker timeout or by a memory leak.

# grid_search.fit(x_train_normalized, y_train) # .round() is temp


# Test its accuracy on the training set using the accuracy_score method.
# Test its accuracy on the test set using the accuracy_score method.

# y_pred_train_svm = grid_search.predict(x_train_normalized)
# y_pred_test_svm = grid_search.predict(x_test_normalized)

# print("\nSVM Training Accuracy:" + str(accuracy_score(y_train, y_pred_train_svm)))
# print("SVM Testing Accuracy:" + str(accuracy_score(y_test, y_pred_test_svm)))


# Tune the hyper-parameters 'C' and 'kernel' (use rbf and linear).
#       Print the best params, using .best_params_, and print the best score, using .best_score_.

# GET BEST  and BEST SCORE

# SVM - Highest mean testing/cross-validated accuracy (best score):   Use x_test_normalized
# SVM - Mean train score: 
# SVM Mean fit time: 



# end_time = time.time() # datetime.datetime.now()
# print ('SVM Done. Time Cost: %d\n' % (end_time - start_time))

# sorted(grid_search.cv_results_.keys()) # Does not display anything.

# print("SVM Best parameters set:")
# best_parameters=grid_search.best_estimator_.get_params()
# for param_name in sorted(parameters.keys()):
    # print("%s: %r" % (param_name, best_parameters[param_name]))

# print("\n\rHighest mean testing/cross-validated accuracy (best score): %0.3f" % grid_search.best_score_)

# Does not change
# print("SVM - Mean train score: " + str(grid_search.cv_results_.get("mean_train_score")));

# Changes every time
# print("SVM Mean fit time: " + str(grid_search.cv_results_.get("mean_fit_time")));

# print("rf_tune Mean fit time: " + str(rf_tune.cv_results_.get("mean_fit_time")));


# Display all (includes two above)
#print("\nSVM grid_search.cv_results_ dict:");
#for key,val in grid_search.cv_results_.items():
#    print (key, ":\n", val)
#print("\n");


# ######################################### Principal Component Analysis #################################################
# Perform dimensionality reduction of the data using PCA.
#       Set parameters n_component to 10 and svd_solver to 'full'. Keep other parameters at their default value.
#       Print the following arrays:
#       - Percentage of variance explained by each of the selected components
#       - The singular values corresponding to each of the selected components.
# print("\n\r----------------------")
# print("Principal Component Analysis (PCA)")

# Linear dimensionality reduction using Singular Value Decomposition (SVD) 
# of the data to project it to a lower dimensional space.

# Piaza: Decomposition performed on the whole X to get the principal components over the entire dataset.

# Eigenvectors (aka: characteristic vectors) are a special set of vectors associated with a linear system of equations 
# (i.e., a matrix equation) for computing the best unique features to describe the samples.

# Pokemon sample
# http://benalexkeen.com/principle-component-analysis-in-python/

# Reducing features down to 10 principle components as stated in instructions above.
# pca = PCA(n_components=10,svd_solver='full')
#pca = PCA(copy=True, iterated_power='auto', n_components=2, random_state=None, svd_solver='full', tol=0.0, whiten=False)

# pca.fit(data) # Use whole dataset based on Piaza.

# 'PCA' object has no attribute 'predict'
#y_pred_test_pca = pca.predict(x_test)
#print('PCA Test Accuracy: ' + str(accuracy_score(y_test, y_pred_test_pca))) # Was 0.8916332888295505

#for param_name in sorted(pca.important_features.keys()):
#    print("\t%s: %r" % (param_name, pca.explained_variance_[param_name]))

# X_pca = pca.transform(data)
# print("original shape:   ", data.shape)
# print("transformed shape:", X_pca.shape)

# print("\npca.explained_variance_ratio_ " + str(pca.explained_variance_ratio_))
#print("pca.components_ " + str(pca.components_))

# print("\npca.singular_values_ " + str(pca.singular_values_))


