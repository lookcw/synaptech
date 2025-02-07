pfrom sklearn.neighbors import KNeighborsClassifier
from write_accuracy_to_file import write_accuracy_to_file
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression, LogisticRegressionCV
from sklearn.ensemble.gradient_boosting import GradientBoostingClassifier
from get_XReduced import get_XReduced
from recursiveFeatureElim import recursiveFeatureElim
from svm import svm_func
import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv
import time
# from ASD_features import extractASDFeatures
# from WTcoef import extractWaveletFeatures
from createFeatureSet import createFeatureSet
from createMatrixFeatureSet import createMatrixFeatureSet
import pearson_features
import granger_features
import domFreq_features
import domFreqVar_features
import raw_features
# import feature_steepness
import FSL_features
import pac_features
from compute_score import compute_group_score
from nn_keras import nn_keras
from nn_Recurr import nn_Recurr
import random
from sklearn.utils import shuffle
import functools
from feature_ranking import get_feature_importance
from identifier import paramToFilename, recurrParamToFilename
from sklearn.ensemble import ExtraTreesClassifier, RandomForestClassifier, GradientBoostingClassifier
from group import file_2_recurr_X
from shuffle_data import shuffle_data
#from nn_Recurr import nn_Recurr


featureName = ''
data_type = ''
hc = False
ad = False
dlb = False
num_epochs = 0  # per patient
num_timePoints = 0  # per instance
num_instances = 0
epochs_per_instance = 0
startAtFS = False
FS = True  # feature selection
RECURR = False

for i in range(1, len(sys.argv), 2):
    if str(sys.argv[i]) == "-h":
        helpString = ('Run pipeline starting from beginning:\nInput arguments:\n-d: data type (choices: Brazil, Greece)' +
                      '\n-f: feature name (choices: ASD, Wavelet, FSL, Steepness)\n-i: instances per patient (ex: 1)\n-t: number of time points per instance (ex: 60)' +
                      '\n-nfs: no feature selection\n-recurr: use LSTM' + '\n-c1: class (HC, AD, DLB)' + '\n-c2: class (HC, AD, DLB)' +
                      '\n\nRun Pipeline With Existing Feature Set:\nInput arguments:\n-fs: feature set (.../PathToFeatureSetFile)')
        print(helpString)
        sys.exit()

    elif str(sys.argv[i]) == "-d":
        data_type = sys.argv[i+1]
        if data_type != 'Brazil' and data_type != 'Greece' and data_type != 'newBrazil' and data_type != 'AR' and data_type != 'Newcastle' and data_type != 'Neuronetrix':
            print("Invalid type of data. Choose from list in help documentation")
            sys.exit()
    elif str(sys.argv[i]) == "-p":
        data_folder_path2 = sys.argv[i+1]
    elif str(sys.argv[i]) == "-n":
        data_folder_path1 = sys.argv[i+1]
    elif str(sys.argv[i]) == "-c1":
        classification = sys.argv[i+1]
        if classification == 'HC':
            hc = True
        elif classification == 'AD':
            ad = True
        elif classification == 'DLB':
            dlb = True
    elif str(sys.argv[i]) == "-c2":
        classification = sys.argv[i+1]
        if classification == 'HC':
            hc = True
        elif classification == 'AD':
            ad = True
        elif classification == 'DLB':
            dlb = True
    elif str(sys.argv[i]) == "-e":
        epochs_per_instance = int(sys.argv[i+1])

    elif str(sys.argv[i]) == "-f":
        featureName = sys.argv[i+1]

    elif str(sys.argv[i]) == "-i":
        num_instances = int(sys.argv[i+1])
        if num_instances == 0:
            print("Did not input instances per patient argument (-p)")
            sys.exit()

    elif str(sys.argv[i]) == "-t":
        num_timePoints = int(sys.argv[i+1])
    elif str(sys.argv[i]) == "-nfs":
        FS = False
    elif str(sys.argv[i]) == "-recurr":
        RECURR = True
    elif str(sys.argv[i]) == "-fs":
        features_path = sys.argv[i+1]
        filename = features_path.split('/')[-1]
        startAtFS = True
    else:
        print(sys.argv[i])
        print("Wrong format. Remember header must precede argument provided.\nUse -h for help.")
        sys.exit()

num_epochs = num_instances * epochs_per_instance

# If starting at the beginning - at feature set creation
if not startAtFS:
    if data_type == '' and not data_folder_path1 and not data_folder_path2:
        print("Did not input data type. Choose from list in help documentation")
        sys.exit()
    if data_type != '' and  data_type != 'Brazil' and data_type != 'Greece' and data_type != 'newBrazil' and data_type != 'AR' and data_type != 'Newcastle' and data_type != 'Neuronetrix':
        print("Invalid type of data. Choose from list in help documentation")
        sys.exit()
    if data_type == '' and data_folder_path1 and data_folder_path2:
        num_electrodes = 21
        data_folder_path3 = None
        data_type = data_folder_path1.split('/')[-1] + '-' + data_folder_path2.split('/')[-1]
    if not RECURR:
        if featureName == '':
            print("Did not input feature name argument (-f)")
            # sys.exit()
    if num_epochs == 0:
        print("Did not input instances per patient argument (-i)")
        # sys.exit()
    if num_timePoints == 0:
        print("Did not input time points argument (-t)\nUse -h for help.")
        sys.exit()
    if featureName == 'Raw':
        extractFeatureFunc = functools.partial(createMatrixFeatureSet, raw_features, featureName)
    if not RECURR:
        if featureName == 'ASD':
            extractFeatureFunc = extractASDFeatures
        # elif featureName == 'Wavelet':
            # extractFeatureFunc = extractWaveletFeatures
        elif featureName == 'FSL':
            extractFeatureFunc = functools.partial(
                createMatrixFeatureSet, FSL_features, featureName)
        elif featureName == 'Pearson':
            extractFeatureFunc = functools.partial(
                createMatrixFeatureSet, pearson_features, featureName)
        elif featureName == 'Granger':
            extractFeatureFunc = functools.partial(
                createMatrixFeatureSet, granger_features, featureName)
        elif featureName == 'DomFreq':
            extractFeatureFunc = functools.partial(
                createMatrixFeatureSet, domFreq_features, featureName)
        elif featureName == 'DomFreqVar':
            extractFeatureFunc = functools.partial(
                createMatrixFeatureSet, domFreqVar_features, featureName)
        elif featureName == 'Steepness':
            extractFeatureFunc = functools.partial(
                createMatrixFeatureSet, feature_steepness, featureName)
        elif featureName == 'PAC':
            extractFeatureFunc = functools.partial(
                createMatrixFeatureSet, pac_features, featureName)
        elif featureName == 'Raw':
            extractFeatureFunc = functools.partial(
                createMatrixFeatureSet, raw_features, featureName)
        else:
            print("Invalid feature name. Choose from list in help documentation")
            sys.exit()

    # feature extraction
    print("Creating Feature Set...")

    if (RECURR):
        features_path = sys.path[0] + '/FeatureSets/' + recurrParamToFilename(
            featureName, data_type, num_instances, num_timePoints, epochs_per_instance)
    else:
        # unique identifier for different input parameters
        features_path = sys.path[0] + '/FeatureSets/' + paramToFilename(
            featureName, data_type, num_instances, num_timePoints, epochs_per_instance)

    # define features and reduced_features paths
    reduced_features_path = sys.path[0] + '/ReducedFeatureSets/' + paramToFilename(
        featureName, data_type, num_instances, num_timePoints, epochs_per_instance)

    # create feature set if does not exist in Feature Sets folder
    if not os.path.exists(features_path):
        print("feature file dne, making it now")
        # 3rd parameter is extractFeature function of choice
        if (data_type == 'Brazil'):
            data_folder_path1 = 'BrazilRawData/HCF50'
            data_folder_path2 = 'BrazilRawData/ADF50'
            data_folder_path3 = None
            num_electrodes = 21

        if (data_type == 'Greece'):
            data_folder_path1 = '.../PathToGreeceHC_DataFolder'
            data_folder_path2 = '.../PathToGreeceMCI_DataFolder'
            data_folder_path3 = None
            num_electrodes = 8

        if (data_type == 'newBrazil'):
            data_folder_path1 = 'BrazilRawData/HCF50_new'
            data_folder_path2 = 'BrazilRawData/ADF50_new'
            data_folder_path3 = None
            num_electrodes = 21

        if (data_type == 'AR'):
            data_folder_path1 = 'BrazilRawData/HC_AR'
            data_folder_path2 = 'BrazilRawData/AD_AR'
            data_folder_path3 = None
            num_electrodes = 21

        if (data_type == 'Neuronetrix'):
            data_folder_path1 = '/Users/Anoop/Documents/Synapto/pipeline/Neuronetrix/AD'
            data_folder_path2 = '/Users/Anoop/Documents/Synapto/pipeline/Neuronetrix/HC'
            data_folder_path3 = None
            num_electrodes = 21

        if (data_type == 'Newcastle'):  # Going into Brazil folder for now
            if hc == True and ad == True and dlb != True:
                data_folder_path1 = 'BrazilRawData/HCF50'
                data_folder_path2 = 'BrazilRawData/ADF50'
                data_folder_path3 = None
            elif hc == True and dlb == True and ad != True:
                data_folder_path1 = 'BrazilRawData/HCF50'
                data_folder_path2 = None
                data_folder_path3 = 'BrazilRawData/ADF50'  # Replace w DLB
            elif ad == True and dlb == True and hc != True:
                data_folder_path1 = None
                data_folder_path2 = 'BrazilRawData/ADF50'
                data_folder_path3 = 'BrazilRawData/ADF50'  # Replace w DLB
            else:
                data_folder_path1 = 'BrazilRawData/HCF50'
                data_folder_path2 = 'BrazilRawData/ADF50'
                data_folder_path3 = 'BrazilRawData/ADF50'  # Replace w DLB
            num_electrodes = 21

        if (featureName == 'FSL' or featureName == 'Pearson' or featureName == 'Granger' or featureName == 'DomFreq' or featureName == 'DomFreqVar' or featureName == 'TsFresh' or featureName == 'Steepness'):
            extractFeatureFunc(num_electrodes, num_instances, num_timePoints, epochs_per_instance,
                               data_folder_path1, data_folder_path2, data_folder_path3, features_path, data_type, RECURR)
        elif (RECURR):
            extractFeatureFunc(num_electrodes, num_instances, num_timePoints, epochs_per_instance,
                               data_folder_path1, data_folder_path2, data_folder_path3, features_path, data_type, RECURR)
            #createFeatureSet(num_epochs, num_timePoints, '', '', num_electrodes, 
                #data_folder_path1, data_folder_path2, data_type, features_path, RECURR)
        else:
            #remove this conditional when ASD/Wavelet extractFeatureFunc is updated
            createFeatureSet(num_epochs, num_timePoints, featureName, extractFeatureFunc, num_electrodes,
                             data_folder_path1, data_folder_path2, data_folder_path3, data_type, RECURR)
    else:
        print("Feature set already exists: " + features_path)

    if (data_type == 'Brazil'):
        num_electrodes = 21
    if (data_type == 'Greece'):
        num_electrodes = 8

    data = pd.read_csv(features_path, header='infer', delimiter=',')
else:  # starting pipeline with feature selection
    data = pd.read_csv(features_path, header='infer')

# shuffle rows of dataframe
data = shuffle(data)
data.sample(frac=1).reset_index(drop=True)
# obtain Y using last column
y = data.iloc[:, -1].values
# Function that randomly shuffles y
# y = shuffle_data(y)

groups = data['patient num']

print("groups.shape :" + str(groups.shape))
print(groups)

unique, counts = np.unique(groups, return_counts=True)
# obtain X by dropping last, first, and 2nd columns (label, patient number, and instance number)
X = data.drop(['patient num', 'instance num','instance code', 'class'], axis=1)
# Function that randomly shuffles X (if you want to create randomized data)
# X = shuffle_data(X)

##################################################################################
if (FS):
    # feature selection
    print("Feature Selection...")
    print("Input Shape:", X.shape)

#  get x_reduced code from this file

clf1 = ExtraTreesClassifier()
clf2 = RandomForestClassifier(n_estimators=50, max_features='sqrt')
clf3 = GradientBoostingClassifier()
# add the classifiers to the array
clfs = [clf1, clf2, clf3]
x_reduced = []

for clf in clfs:
	feat_importances_et = get_feature_importance(clf, X, y, 50) #top 50 features
	x_reduced.append(get_XReduced(clf, X))

##################################################################################

# learning model
print("Learning model...")
#from xgboost import XGBClassifier

num_folds = 10
num_seeds = 10
o_filename = 'output_pipeline.csv'


# Megha's svm
#svm_func(X_reduced,y,num_seeds, num_folds, 'output_pipeline.csv')

#nn_keras
nn = nn_keras(X, y, n_hlayers = 3, neurons = [100,100,100],learning_rate = 0.1,n_folds =3,n_classes = 2, seed = 5, grps = groups)


# nn_Recurr
if (RECURR):
	print(features_path)
	SVD_features_path = features_path.split('.')[0] + '_SVD.' + features_path.split('.')[1]
	from SVD import svd
	svd(features_path, 2)
	patient_num, X_3D, y_ = file_2_recurr_X(SVD_features_path)
	#print("SHAPE")
	#print(X_3D.shape)
	nn_recurr = nn_Recurr(X_3D, y, n_hlayers = 3, neurons = [100,50,20],learning_rate = 0.1,n_folds =2,n_classes = 2, seed = 5)

#various sklearn models
logreg = LogisticRegression() 
logreg_cv = LogisticRegressionCV()
rf = RandomForestClassifier()
gboost = GradientBoostingClassifier()
svc = SVC()
kneighbors = KNeighborsClassifier(n_neighbors=5)
# xgboost = XGBClassifier() -> not working

# loop through models and print accuracy for each
if (RECURR):
    models = [nn_recurr, logreg, logreg_cv, rf, gboost, svc, kneighbors]
else:
    models = [logreg, logreg_cv, rf, gboost, svc, kneighbors]
    # models = [nn, logreg, logreg_cv, rf, gboost, svc, kneighbors]
# models = [svc]
# Get and write accuracies to an output csv file
for i in range(0, len(clfs)):
    print(format(clfs[i].__class__))
    print("\n")
    for model in models:
        write_accuracy_to_file(clfs[i], model, groups, x_reduced[i], X, y, num_folds,
                               num_seeds, o_filename, features_path, featureName, data_type)