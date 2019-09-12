import numpy as np
import sys
import os
from numpy import genfromtxt
import pandas as pd


STARTER_COLUMNS = ['instance code','patient num', 'instance num',]
CLASS_COLUMN = ['class']

def write_feature_set(feature_path, feature_set_df):
    print('writing feature set to file')
    feature_set_df.to_csv(feature_path, index=False)


def create_feature_set(CONFIG, config_feature=None):
    print('starting feature set creation')
    (positive_features, patient_count, instance_count) = _get_features_for_folder(CONFIG, CONFIG['positive_folder_path'],
                                                                                  0, 0, 1, config_feature)
    (negative_features, patient_count, instance_count) = _get_features_for_folder(CONFIG, CONFIG['negative_folder_path'], patient_count, 
                                                                                  instance_count, 0, config_feature)
    labels = STARTER_COLUMNS + \
        get_labels_from_folder(CONFIG)\
         + CLASS_COLUMN
    data = np.array(positive_features + negative_features)
    return pd.DataFrame(data=data,  columns = labels)

def get_labels_from_folder(CONFIG):
    whole_data_set = genfromtxt(os.path.join(CONFIG['positive_folder_path'], os.listdir(CONFIG['positive_folder_path'])[0]), delimiter=',')
    epoch_data_set = whole_data_set[0:CONFIG['time_points_per_epoch']]
    return CONFIG['feature_class'].getHeader(epoch_data_set)

def _get_features_for_folder(CONFIG, data_folder, patient_count, instance_count, data_class, config_feature=None):
    filenames = [filename for filename in os.listdir(data_folder)]
    folder_features_with_filenames = [
        _extract_feature_for_one_patient(
            filename,
            genfromtxt(os.path.join(data_folder,filename), delimiter=','),
            CONFIG,
            config_feature
        )
        for filename in os.listdir(data_folder) if filename.endswith('.csv')
    ]
    folder_features = [folder_feature[0] for folder_feature in folder_features_with_filenames]
    filenames = [folder_feature[1] for folder_feature in folder_features_with_filenames]
    return _unpack_add_groups(folder_features, filenames, patient_count, instance_count, data_class)

# def _get_features_for_folder(data_folder, patient_count, instance_count, functionClass, num_instances, epochs_per_instance, time_points_per_epoch, data_class, bands_func):
#     filenames = [filename for filename in os.listdir(data_folder)]
#     folder_features_with_filenames = [
#         _extract_feature_for_one_patient(
#             functionClass,
#             filename,
#             genfromtxt(os.path.join(data_folder,filename), delimiter=','),
#             num_instances,
#             epochs_per_instance,
#             time_points_per_epoch,
#             bands_func
#         )
#         for filename in os.listdir(data_folder) if filename.endswith('.csv')
#     ]
#     folder_features = [folder_feature[0] for folder_feature in folder_features_with_filenames]
#     filenames = [folder_feature[1] for folder_feature in folder_features_with_filenames]
#     return _unpack_add_groups(folder_features, filenames, patient_count, instance_count, data_class)


def _unpack_add_groups(X, filenames, patient_count, instance_count, data_class):
    """Turns 4d array of patients to 2d    
    Arguments:
        X {4D numpy array} -- [description]
        patient_count {[type]} -- [description]
        instance_count {[type]} -- [description]

    Returns:
        [type] -- [description]
    """
    two_d_array = []
    for (patient_data, filename) in zip(X,filenames):
        for instance_data in patient_data:
            for epoch_data in instance_data:
                two_d_array.append([filename.replace('.csv',''), patient_count, instance_count] + epoch_data.tolist() + [data_class])
            instance_count += 1
        patient_count += 1
    return (two_d_array, patient_count, instance_count)


def _extract_feature_for_one_patient(filename, patient_data_set, CONFIG, config_feature=None):
    """applys the extractFeatures function of function class onto one patient's dataset

    Arguments:
        functionClass {module} -- a module with at least 2 public methods, extractFeatures and getHeader
        data_set {np.array} -- 2d numpy array where number of columns is number of electrodes
        num_instances {int} -- number of instances per patient
        epochs_per_instance {int} -- epochs per instance
        time_points_per_epoch {int} -- time points per epoch`

    Keyword Arguments:
        bandsFunc {function} -- A function to apply to each electrode, supposed to be a band pass function (default: {None})

    Returns:
        3d numpy array -- 3d array, where first dimension is across instances, 2nd is across epochs, 3rd is across time points
    """
    print(f'extracting features for {filename}')

    if CONFIG['is_bands']:
        transposed_data_set = np.transpose(patient_data_set)
        transposed_filtered = [config_feature['bands_func'](time_series)
                               for time_series in transposed_data_set]
        patient_data_set = np.transpose(transposed_filtered)
    features = []

    count = 0
    for _ in range(CONFIG['num_instances']):
        instance_features = []
        for _ in range(CONFIG['epochs_per_instance']):
            feature_row = CONFIG['feature_class'].extractFeatures(
                patient_data_set[count*CONFIG['time_points_per_epoch']:(count+1) * CONFIG['time_points_per_epoch']], config_feature)
            instance_features.append(feature_row)
            count += 1
        features.append(instance_features)
    if hasattr(CONFIG['feature_class'], 'apply_after'):
        features = CONFIG['feature_class'].apply_after(features)
    return (np.array(features), filename)
