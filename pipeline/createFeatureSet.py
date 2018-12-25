import csv
import numpy as np
import os
import sys
import pandas as pd
from BandPass1 import splitbands


def createFeatureSet(num_epochs, num_timePoints, featureName, extractFeatures, num_electrodes, path1, path2):

	#extract from path to first patient group folder
	combined_group1 = np.empty((0,num_electrodes*num_timePoints+1+1))
	patient_num = 1
	for filename in os.listdir(path1):
		print patient_num
		if filename.endswith('.csv'):
			with open(os.path.join(path1, filename)) as f:
				reader = csv.reader(f)
				array = np.array(list(reader))
				print(array.shape)
				#print len(array) #160,000
				#print len(array[0]) #21
				data = array

				#create bunches per patient, creates num_bunches of instances, takes care of one patient per iteration
				total = np.empty((num_epochs,(len(array[0]))*(num_timePoints)+1+1)) #1000x630
				for bunch in range(num_epochs):
					index = int(bunch*(len(array)/num_epochs))
					row = data[index:index+num_timePoints].flatten()
					row = np.append(np.insert(row,0,patient_num), [0])
					#print row
					total[bunch] = row
				#print total
				combined_group1 = np.concatenate((combined_group1,total)) #12000x630
				patient_num += 1

	#extract from path to second patient group folder
	combined_group2 = np.empty((0,(num_electrodes)*num_timePoints+1+1))
	for filename in os.listdir(path2):
		if filename.endswith('.csv'):
			with open(os.path.join(path2, filename)) as f:
				reader = csv.reader(f)
				array = list(reader)
				array = np.array(array)
				#print len(array) #160,000
				#print len(array[0]) #21
				data = array

				#create bunches per patient
				total = np.empty((num_epochs,(len(array[0]))*(num_timePoints)+1+1))  #1000x210
				for bunch in range(num_epochs):
					index = int(bunch*(len(array)/num_epochs))
					row = data[index:index+num_timePoints].flatten()
					row = np.append(np.insert(row,0,patient_num), [1])
					#print row
					total[bunch] = row
				#print total
				combined_group2 = np.concatenate((combined_group2,total))
				patient_num += 1

	combined = np.concatenate((combined_group1, combined_group2))
	#print(combined.shape) #25000x631

	#store and delete last column
	targets = combined[:,-1]
	groups = combined[:,0]
	print groups

	combined = np.delete(combined,0,axis=1)
	combined = np.delete(combined,-1,axis=1)
	print combined.shape
	print combined
	#reshape into 25000 x timepoints x 21
	combined = np.reshape(combined,(len(combined), num_timePoints, num_electrodes))


	

	identifier = str(num_epochs) + 'epochs_' + str(num_timePoints) + 'timepoints'

	features_path = sys.path[0] + '/FeatureSets/'+featureName+'features'+identifier+'.csv'

	if not os.path.exists(features_path):
		open(features_path,"w")

	#count number of lines already present in file - start at this number + 1 for iterations
	read_file = open(features_path,"r")
	reader = csv.reader(read_file)
	row_count = sum(1 for row in reader)
	print(row_count)

	out_file = open(features_path,"a") #used to be "a" for append
	writer = csv.writer(out_file)

	print("Feature Extraction...")

	#initialize header list
	headers = []

	#create header list
	for i in range(row_count,len(combined)):
		#transpose each n x 21 so each row is time series points (columns) of 1 electrode (row)
		transposed = np.transpose(combined[i]) 
		#add another dimension in each row to make it 5 bands x n
		for j in range(len(transposed)):
			if (i==0):
				bands = splitbands(transposed[j])
			#squish each band of raw points into n feature values
			for k in range(len(bands)): #bands[j] = band of raw data
				if (j==0):
					bandfeatures = extractFeatures(bands[k])
				#adding headers
				if (i == 0):
					featureHeaders = []
					for h in range(len(bandfeatures)):
						featureHeaders.append(("electrode"+str(j+1)+"band"+str(k+1)+"feature"+str(h+1)))
					headers.extend(featureHeaders)

	headers.append('class')
	writer.writerow(headers)

	for i in range(row_count,len(combined)):
		print(str(i+1) + " out of " + str(25*num_epochs))
		#transpose each n x 21 so each row is time series points (columns) of 1 electrode (row)
		transposed = np.transpose(combined[i]) 
		features = [groups[i]]

		#add another dimension in each row to make it 5 bands x n
		for j in range(len(transposed)):
			bands = splitbands(transposed[j])
			#squish each band of raw points into n feature values
			for k in range(len(bands)): #bands[j] = band of raw data
				bandfeatures = extractFeatures(bands[k])
				features.extend(bandfeatures)

				#adding headers
				if (i == 0):
					featureHeaders = []
					for h in range(len(bandfeatures)):
						featureHeaders.append(("electrode"+str(j+1)+"band"+str(k+1)+"feature"+str(h+1)))
					headers.extend(featureHeaders)

		features.append(targets[i])
		#Add feature values of each band from each electrode (per instance) to new array
		writer.writerow(features)