def paramToFilename(feature_name, config_identifier , datatype, num_instances ,num_timePoints, epochs_per_instance):
    return feature_name +'-'+ config_identifier + "_" + str(datatype) + "_" + str(num_instances)+'_instances_'+ str(epochs_per_instance) + '_epochs_' + str(num_timePoints) + '_timepoints.csv'
def curry_param_to_filename(datatype, num_instances ,num_timePoints, epochs_per_instance):
    return (lambda feature_name, config_identifier: paramToFilename(feature_name, config_identifier, datatype,num_instances,num_timePoints,epochs_per_instance))
def recurrParamToFilename(feature_name, datatype, num_instances ,num_timePoints, epochs_per_instance):
    return feature_name +"_" + str(datatype) + "_" + str(num_instances)+'_instances_'+ str(epochs_per_instance) + '_epochs_' + str(num_timePoints) + '_timepoints_recurr.csv'
def filenameToParam(filename):
    line = filename.split('_')
    #feature_name, datatype, num_instances, epochs,timepoints
    return ('_'.join(line[:-7]),line[-7],int(line[-6]),int(line[-4]),int(line[-2]))