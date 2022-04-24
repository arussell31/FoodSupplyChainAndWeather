#import libraries
import pkg_resources
from pkg_resources import DistributionNotFound, VersionConflict
from platform import python_version
import numpy as np
import pandas as pd
import time
import gc
import random
from sklearn.model_selection import cross_val_score, GridSearchCV, cross_validate, train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.svm import SVC
from sklearn.linear_model import LinearRegression
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, normalize
from sklearn.decomposition import PCA
from sklearn.impute import SimpleImputer
from sklearn.metrics import r2_score
from sklearn.preprocessing import PolynomialFeatures
import os
from sklearn.preprocessing import StandardScaler
from sklearn import linear_model
import csv
import statistics
from sklearn.model_selection import cross_val_predict
from sklearn.model_selection import cross_val_score
from statistics import mean
from sklearn.feature_selection import mutual_info_regression
from numpy import arange
from pandas import read_csv
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import RepeatedKFold
from sklearn.linear_model import ElasticNet

def getData(path):
    x_data_continuous = pd.read_csv(path,usecols=['precip_0', 'precip_1', 'precip_2', 'precip_3', 'precip_4', 'precip_5', 'precip_6', 'precip_7', 'precip_8', 'precip_9', 'precip_10', 'precip_11', 'precip_12', 'precip_13', 'precip_14', 'precip_15', 'precip_16', 'precip_17', 'precip_18', 'precip_19', 'precip_20', 'precip_21', 'precip_22', 'precip_23', 'min_temp_0', 'min_temp_1', 'min_temp_2', 'min_temp_3', 'min_temp_4', 'min_temp_5', 'min_temp_6', 'min_temp_7', 'min_temp_8', 'min_temp_9', 'min_temp_10', 'min_temp_11', 'min_temp_12', 'min_temp_13', 'min_temp_14', 'min_temp_15', 'min_temp_16', 'min_temp_17', 'min_temp_18', 'min_temp_19', 'min_temp_20', 'min_temp_21', 'min_temp_22', 'min_temp_23', 'max_temp_0', 'max_temp_1', 'max_temp_2', 'max_temp_3', 'max_temp_4', 'max_temp_5', 'max_temp_6', 'max_temp_7', 'max_temp_8', 'max_temp_9', 'max_temp_10', 'max_temp_11', 'max_temp_12', 'max_temp_13', 'max_temp_14', 'max_temp_15', 'max_temp_16', 'max_temp_17', 'max_temp_18', 'max_temp_19', 'max_temp_20', 'max_temp_21', 'max_temp_22', 'max_temp_23', 'avg_temp_0', 'avg_temp_1', 'avg_temp_2', 'avg_temp_3', 'avg_temp_4', 'avg_temp_5', 'avg_temp_6', 'avg_temp_7', 'avg_temp_8', 'avg_temp_9', 'avg_temp_10', 'avg_temp_11', 'avg_temp_12', 'avg_temp_13', 'avg_temp_14', 'avg_temp_15', 'avg_temp_16', 'avg_temp_17', 'avg_temp_18', 'avg_temp_19', 'avg_temp_20', 'avg_temp_21', 'avg_temp_22', 'avg_temp_23', 'Agricultural Land Mass'])
    x_data_discrete = pd.read_csv(path,usecols=['flood_0', 'flood_1', 'flood_2', 'flood_3', 'flood_4', 'flood_5', 'flood_6', 'flood_7', 'flood_8', 'flood_9', 'flood_10', 'flood_11', 'flood_12', 'flood_13', 'flood_14', 'flood_15', 'flood_16', 'flood_17', 'flood_18', 'flood_19', 'flood_20', 'flood_21', 'flood_22', 'flood_23', 'drought_0', 'drought_1', 'drought_2', 'drought_3', 'drought_4', 'drought_5', 'drought_6', 'drought_7', 'drought_8', 'drought_9', 'drought_10', 'drought_11', 'drought_12', 'drought_13', 'drought_14', 'drought_15', 'drought_16', 'drought_17', 'drought_18', 'drought_19', 'drought_20', 'drought_21', 'drought_22', 'drought_23', 'disaster_0', 'disaster_1', 'disaster_2', 'disaster_3', 'disaster_4', 'disaster_5', 'disaster_6', 'disaster_7', 'disaster_8', 'disaster_9', 'disaster_10', 'disaster_11', 'disaster_12', 'disaster_13', 'disaster_14', 'disaster_15', 'disaster_16', 'disaster_17', 'disaster_18', 'disaster_19', 'disaster_20', 'disaster_21', 'disaster_22', 'disaster_23'])
    y_data = pd.read_csv(path,usecols=['Yield'])
    y_data = y_data.squeeze()
    return x_data_continuous, x_data_discrete, y_data

def polynomial(x_data_continuous):
    poly = PolynomialFeatures(degree=2, include_bias=False)
    x_continuous_polynomial = poly.fit_transform(x_data_continuous)
    columnNames = poly.get_feature_names_out(x_data_continuous.columns)
    x_continuous_polynomial = pd.DataFrame(x_continuous_polynomial, columns = columnNames)
    #pd.DataFrame(x_continuous_polynomial).to_csv("test.csv")
    return x_continuous_polynomial, columnNames

def joinCAndD(x_continuous, x_discrete):
    #concatenate continuous and disrete dataframes back together horizontally before splitting into train and test sets
    #convert np arrays to dataframes
    x_continuous = pd.DataFrame(x_continuous)
    x_discrete = pd.DataFrame(x_discrete)
    #concatenate dataframes horizontally
    joined = pd.concat([x_continuous, x_discrete], axis=1)
    return joined

def splitTrainTest(x_data,y_data,testSize):
    #split the data into train and test sets
    x_train, x_test, y_train, y_test = train_test_split(x_data, y_data, test_size=testSize, shuffle=True)
    return x_train, x_test, y_train, y_test

def splitCAndD(x_train, x_test, continuousCols):
    #divide the train and test data based on whether it's continuous or discrete
    x_train_continuous = x_train[continuousCols]
    x_train_discrete = x_train[['flood_0', 'flood_1', 'flood_2', 'flood_3', 'flood_4', 'flood_5', 'flood_6', 'flood_7', 'flood_8', 'flood_9', 'flood_10', 'flood_11', 'flood_12', 'flood_13', 'flood_14', 'flood_15', 'flood_16', 'flood_17', 'flood_18', 'flood_19', 'flood_20', 'flood_21', 'flood_22', 'flood_23', 'drought_0', 'drought_1', 'drought_2', 'drought_3', 'drought_4', 'drought_5', 'drought_6', 'drought_7', 'drought_8', 'drought_9', 'drought_10', 'drought_11', 'drought_12', 'drought_13', 'drought_14', 'drought_15', 'drought_16', 'drought_17', 'drought_18', 'drought_19', 'drought_20', 'drought_21', 'drought_22', 'drought_23', 'disaster_0', 'disaster_1', 'disaster_2', 'disaster_3', 'disaster_4', 'disaster_5', 'disaster_6', 'disaster_7', 'disaster_8', 'disaster_9', 'disaster_10', 'disaster_11', 'disaster_12', 'disaster_13', 'disaster_14', 'disaster_15', 'disaster_16', 'disaster_17', 'disaster_18', 'disaster_19', 'disaster_20', 'disaster_21', 'disaster_22', 'disaster_23']]
    x_test_continuous = x_test[continuousCols]
    x_test_discrete = x_test[['flood_0', 'flood_1', 'flood_2', 'flood_3', 'flood_4', 'flood_5', 'flood_6', 'flood_7', 'flood_8', 'flood_9', 'flood_10', 'flood_11', 'flood_12', 'flood_13', 'flood_14', 'flood_15', 'flood_16', 'flood_17', 'flood_18', 'flood_19', 'flood_20', 'flood_21', 'flood_22', 'flood_23', 'drought_0', 'drought_1', 'drought_2', 'drought_3', 'drought_4', 'drought_5', 'drought_6', 'drought_7', 'drought_8', 'drought_9', 'drought_10', 'drought_11', 'drought_12', 'drought_13', 'drought_14', 'drought_15', 'drought_16', 'drought_17', 'drought_18', 'drought_19', 'drought_20', 'drought_21', 'drought_22', 'drought_23', 'disaster_0', 'disaster_1', 'disaster_2', 'disaster_3', 'disaster_4', 'disaster_5', 'disaster_6', 'disaster_7', 'disaster_8', 'disaster_9', 'disaster_10', 'disaster_11', 'disaster_12', 'disaster_13', 'disaster_14', 'disaster_15', 'disaster_16', 'disaster_17', 'disaster_18', 'disaster_19', 'disaster_20', 'disaster_21', 'disaster_22', 'disaster_23']]
    return x_train_continuous, x_train_discrete, x_test_continuous, x_test_discrete

def splitCAndDFiltered(x_train, x_test, filteredCols):
    #divide the train and test data based on whether it's continuous or discrete
    discreteCols = ['flood_0', 'flood_1', 'flood_2', 'flood_3', 'flood_4', 'flood_5', 'flood_6', 'flood_7', 'flood_8', 'flood_9', 'flood_10', 'flood_11', 'flood_12', 'flood_13', 'flood_14', 'flood_15', 'flood_16', 'flood_17', 'flood_18', 'flood_19', 'flood_20', 'flood_21', 'flood_22', 'flood_23', 'drought_0', 'drought_1', 'drought_2', 'drought_3', 'drought_4', 'drought_5', 'drought_6', 'drought_7', 'drought_8', 'drought_9', 'drought_10', 'drought_11', 'drought_12', 'drought_13', 'drought_14', 'drought_15', 'drought_16', 'drought_17', 'drought_18', 'drought_19', 'drought_20', 'drought_21', 'drought_22', 'drought_23', 'disaster_0', 'disaster_1', 'disaster_2', 'disaster_3', 'disaster_4', 'disaster_5', 'disaster_6', 'disaster_7', 'disaster_8', 'disaster_9', 'disaster_10', 'disaster_11', 'disaster_12', 'disaster_13', 'disaster_14', 'disaster_15', 'disaster_16', 'disaster_17', 'disaster_18', 'disaster_19', 'disaster_20', 'disaster_21', 'disaster_22', 'disaster_23']
    filteredContinuousCols = []
    filteredDiscreteCols = []
    for c in filteredCols:
        if c in discreteCols:
            filteredDiscreteCols.append(c)
        else:
            filteredContinuousCols.append(c)
    x_train_continuous = x_train[filteredContinuousCols]
    x_train_discrete = x_train[filteredDiscreteCols]
    x_test_continuous = x_test[filteredContinuousCols]
    x_test_discrete = x_test[filteredDiscreteCols]
    return x_train_continuous, x_train_discrete, x_test_continuous, x_test_discrete

def scaleData(x_train_continuous, x_test_continuous,continuousCols):
    #scale the continuous data only. it doesn't make sense to scale dummy / binary discrete values
    #fit the scaler to the training data only, then apply the scaler to test data. do not scale to all data or test data.
    scaler = StandardScaler()
    x_train_c_scaled = pd.DataFrame(scaler.fit_transform(x_train_continuous), columns = continuousCols, index=x_train_continuous.index) #MUST PUT INDEX = ... OR IT WILL NOT MAINTAIN THE SHUFFLED INDICES BUT WILL REWRITE OVER THEM
    x_test_c_scaled = pd.DataFrame(scaler.transform(x_test_continuous), columns = continuousCols, index=x_test_continuous.index) #MUST PUT INDEX = ... OR IT WILL NOT MAINTAIN THE SHUFFLED INDICES BUT WILL REWRITE OVER THEM
    return x_train_c_scaled, x_test_c_scaled

def classicLinearRegression(x_train, x_test, y_train, y_test):
    regressor = LinearRegression()
    model = regressor.fit(x_train, y_train)
    y_predict_train = model.predict(x_train)
    y_predict_test = model.predict(x_test)
    r_sq_train = r2_score(y_train, y_predict_train)
    r_sq_test = r2_score(y_test, y_predict_test)
    intercept = model.intercept_
    coefficients = model.coef_
    return r_sq_train, r_sq_test, intercept, coefficients

def lassoRegression(x_train, x_test, y_train, y_test,a,m,t):
    clf = linear_model.Lasso(alpha=a, max_iter=m, tol=t)
    model = clf.fit(x_train, y_train)
    y_predict_train = model.predict(x_train)
    y_predict_test = model.predict(x_test)
    r_sq_train = r2_score(y_train, y_predict_train)
    r_sq_test = r2_score(y_test, y_predict_test)
    intercept = model.intercept_
    coefficients = model.coef_
    return r_sq_train, r_sq_test, intercept, coefficients

def mutualInfoFilter(x_data, y_data, mi):
    mutual_info = mutual_info_regression(x_data,y_data)
    mi_score_selected_index = np.where(mutual_info >mi)[0]
    x_data_filtered = x_data.iloc[:,mi_score_selected_index]
    filtered_col_names = x_data_filtered.columns
    return x_data_filtered,y_data, filtered_col_names 

def getEquation(coefficients,intercept,columnHeaders):
    coefficientsNoZerosIndex = np.where(abs(coefficients) != 0 )[0]
    coefficientsNoZeros = coefficients[coefficientsNoZerosIndex]
    coefficientsNoZeros = np.insert(coefficientsNoZeros,0,intercept)
    columnHeadersNoZeros = np.asarray(columnHeaders[coefficientsNoZerosIndex])
    columnHeadersNoZeros = np.insert(columnHeadersNoZeros,0,"intercept")
    return columnHeadersNoZeros,coefficientsNoZeros

def getCountryAndCropNames(f):
    fileOnly = f.split("/")[-1]
    fList = fileOnly.split("-")
    country = fList[0]
    crop = fList[1]
    return country,crop

def createDataframeLeaveZeros(coefficients,intercept,columnHeaders):
    columnHeaders = np.insert(columnHeaders,0,"intercept")
    coefficients = np.insert(coefficients,0,intercept)
    allCoefficientsDF = pd.DataFrame(models, columns = columnHeaders)
    return allCoefficientsDF


lasso_params = [0.02, 0.5, 0.8, 2, 8, 20, 30, 50, 100, 200, 400]
mutualInfoMinimum = [0.2,0.3,0.4,0.5,0.6]

directory = 'output'
#directory = 'src/tryit'
r_sq_list = []
countGood = 0
countBad = 0
count = 0
filesToSkip = []
#skip files where data is incomplete (years don't span 1961 to 2018)
for filename in os.listdir(directory):
    count += 1
    if count <= 2572:
        f = os.path.join(directory, filename)
        # checking if it is a file
        if os.path.isfile(f):
            x_data_continuous, x_data_discrete, y_data = getData(f)
            try:
                if len(y_data) < 58:
                    countBad += 1
                    filesToSkip.append(f)
                else:
                    countGood += 1
            except:
                countBad += 1
                filesToSkip.append(f)
print("countGood: ", countGood)
print("countBad: ", countBad)
print("len(filesToSkip): ", len(filesToSkip))

#choose 100 random files
#randomList = []
#for i in range(0,100):
#    n = random.randint(1,2572)
#    randomList.append(n)

models = {}
final = {}
#bestR2List = []
count = 0
for filename in os.listdir(directory):
    count += 1
    if count <= 2572:
        f = os.path.join(directory, filename)
        # checking if it is a file
        if os.path.isfile(f):
            if f not in filesToSkip:
                results = {}
                equations = {}
                x_data_continuous, x_data_discrete, y_data = getData('output/Afghanistan-Apples-final_out.csv')
                x_continuous_polynomial, polycols = polynomial(x_data_continuous)
                joined = joinCAndD(x_continuous_polynomial,x_data_discrete)
                x_train, x_test, y_train, y_test = splitTrainTest(joined,y_data,0.2)
                x_train_continuous, x_train_discrete, x_test_continuous, x_test_discrete = splitCAndD(x_train, x_test, polycols)
                x_train_c_scaled, x_test_c_scaled = scaleData(x_train_continuous, x_test_continuous,polycols)
                x_train_scaled = joinCAndD(x_train_c_scaled, x_train_discrete)
                x_test_scaled = joinCAndD(x_test_c_scaled,x_test_discrete)

                k = "classic_linear_regression"
                r_sq_train, r_sq_test, intercept, coefficients = classicLinearRegression(x_train_scaled, x_test_scaled, y_train, y_test)
                
                results[k] = r_sq_test
                columnHeadersNoZeros,coefficientsNoZeros = getEquation(coefficients,intercept,x_train_scaled.columns)
                
                equations[k]={}
                equations[k]["cols"] = columnHeadersNoZeros
                equations[k]["coeffs"] = coefficientsNoZeros
                
                for alpha in lasso_params:
                    k = "lasso_" + str(alpha)
                    r_sq_train, r_sq_test, intercept, coefficients = lassoRegression(x_train_scaled, x_test_scaled, y_train, y_test,alpha,10000,0.0001)
                    results[k] = r_sq_test
                    columnHeadersNoZeros,coefficientsNoZeros = getEquation(coefficients,intercept,x_train_scaled.columns)
                    #equations[k] = [columnHeadersNoZeros,coefficientsNoZeros]
                    equations[k]={}
                    equations[k]["cols"] = columnHeadersNoZeros
                    equations[k]["coeffs"] = coefficientsNoZeros

                #repeat with x data filtered using mutual info regression:
                
                for mi in mutualInfoMinimum:
                    try:
                        x_data_filtered,y_data, filtered_col_names = mutualInfoFilter(joined, y_data,mi)
                        x_train, x_test, y_train, y_test = splitTrainTest(x_data_filtered,y_data,0.2)
                        x_train_continuous, x_train_discrete, x_test_continuous, x_test_discrete = splitCAndDFiltered(x_train, x_test, filtered_col_names)
                        x_train_c_scaled, x_test_c_scaled = scaleData(x_train_continuous, x_test_continuous,filtered_col_names)
                        x_train_scaled = joinCAndD(x_train_c_scaled, x_train_discrete)
                        x_test_scaled = joinCAndD(x_test_c_scaled,x_test_discrete)

                        k = "mir_" + str(mi) + "_classic_linear_regression"
                        r_sq_train, r_sq_test, intercept, coefficients =  classicLinearRegression(x_train_scaled, x_test_scaled, y_train, y_test)
                        results[k] = r_sq_test
                        columnHeadersNoZeros,coefficientsNoZeros = getEquation(coefficients,intercept,x_train_scaled.columns)
                        #equations[k] = [columnHeadersNoZeros,coefficientsNoZeros]
                        equations[k]={}
                        equations[k]["cols"] = columnHeadersNoZeros
                        equations[k]["coeffs"] = coefficientsNoZeros

                        for alpha in lasso_params:
                            k = "mir_" + str(mi) + "_lasso_" + str(alpha)
                            r_sq_train, r_sq_test, intercept, coefficients = lassoRegression(x_train_scaled, x_test_scaled, y_train, y_test,alpha,10000,0.0001)
                            results[k] = r_sq_test
                            columnHeadersNoZeros,coefficientsNoZeros = getEquation(coefficients,intercept,x_train_scaled.columns)
                            equations[k]={}
                            equations[k]["cols"] = columnHeadersNoZeros
                            equations[k]["coeffs"] = coefficientsNoZeros
                    except ValueError: #if this error is thrown, our mi value was so high that all columns were filtered out
                        pass 

                bestR2 = max(results.values())
                bestModel = max(results, key=results.get)
                if bestModel not in models.keys():
                    models[bestModel] = 0
                models[bestModel] += 1
                #bestR2List.append(bestR2)

                #write final model for this crop/country combination to its own csv:
                finalModelCols = np.array(equations[bestModel]["cols"])
                finalModelCoeffs = pd.DataFrame(equations[bestModel]["coeffs"]).transpose()
                newColNameDict = {}
                for i in range(0,len(finalModelCols)):
                    newColNameDict[i] = finalModelCols[i]
                modelDF = finalModelCoeffs.rename(columns=newColNameDict)
                country, crop = getCountryAndCropNames(f)
                outputFileName = "final_models/" + country+ "_" + crop + ".csv"
                countryCropKey = country + "_" + crop
                modelDF.to_csv(outputFileName)

                
                if country not in final.keys():
                    final[country] = {}
                final[country][crop] = {}
                final[country][crop]['bestR2'] = bestR2
                final[country][crop]['bestModel'] = bestModel

                print(country," ",crop)
                print(country," ",crop)
                print(country," ",crop)
        

#print(final)
#print(models)
#print(bestR2List)
#print(modelDF)

#write csv that includes each type of model and how many times it was used as "the best" choice
modelRankDF = pd.DataFrame(models, index=["times_used"])
modelRankDF = modelRankDF.transpose()
modelRankDF.to_csv("final_models/modelsRanked.csv")

#write csv with columns: country, crop, best model type, R2
allModelsDF = pd.DataFrame(columns=['Country', 'Crop', 'Model_Type', 'R2'])
for key,value in final.items():
    country = key
    for k,v in value.items():
        crop = k
        r2 = value[crop]['bestR2']
        modelType = value[crop]['bestModel']
        allModelsDF = allModelsDF.append({'Country': country, 'Crop': crop, 'Model_Type': modelType, 'R2':r2}, ignore_index=True)
allModelsDF.to_csv("final_models/allModelsDF.csv")