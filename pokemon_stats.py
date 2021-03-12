#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import numpy as np
import math
import random
import matplotlib.pyplot as plt

# Takes in a string to a CSV file, returns first 20 data points
# without Generation and Legendary columns, in a single structure
def load_data(filepath):
	with open(filepath, newline='') as csvfile:
		reader = csv.DictReader(csvfile)
		count = 0
		retList = []
		for row in reader:
			if count >= 20:
				break

			row.pop('Generation')
			row.pop('Legendary')
			row['#'] = int(row['#'])
			row['Total'] = int(row['Total'])
			row['HP'] = int(row['HP'])
			row['Attack'] = int(row['Attack'])
			row['Defense'] = int(row['Defense'])
			row['Sp. Atk'] = int(row['Sp. Atk'])
			row['Sp. Def'] = int(row['Sp. Def'])
			row['Speed'] = int(row['Speed'])

			retList.append(row)
			count += 1
		return retList

# Takes in one row of data loaded from the previous function, calcs
# corresponding x and y and returns them in a single structure
def calculate_x_y(stats):
	attack = stats['Attack'] + stats['Sp. Atk'] + stats['Speed']
	defense = stats['Defense'] + stats['Sp. Def'] + stats['HP']
	pokeTuple = (attack, defense)
	return pokeTuple
	

# performs single linkage hierarchical agglomerative clustering on 
# the pokemon with the x,y feature representation, and returns a data
# structure representing the clustering
def hac(dataset):
	m = len(dataset)
	clusters = {}
	dists = {}
	Z = []
	dataset = [dataset[i] for i in range(m) if np.all(np.isfinite(dataset[i]))]
	m = len(dataset)

	# put all the data into a dict in the form [clustNum: [(x,y)]]
	for i in range(0, m):
		clustNum = str(i)
		clusters[clustNum] = [dataset[i]]

	# store original distances in the form ['clustNum1:clustNum2': dist]
	# this will help us later
	for clustNum1, clustVal1 in clusters.items():
		for clustNum2, clustVal2 in clusters.items():
			# skip ahead if we are comparing the same cluster
			if clustNum1 == clustNum2: continue
			dists[clustNum1 + ':' + clustNum2] = euclidean_dist(clustVal1[0], clustVal2[0])

	while len(clusters) > 1:

		minDist = min(dists.values())
		closestClusterNums = [key for key in dists if dists[key] == minDist]
		
		# some arbitrarily large number we can use to help with tie breaking
		mrg1 = mrg2 = 99999999

		# tie breakers
		for smallest in closestClusterNums:
			smallest = smallest.replace(':', ' ')
			numbers = [int(s) for s in smallest.split() if s.isdigit()]
			if numbers[0] <= mrg1:
				mrg1 = numbers[0]
				if numbers[1] < mrg2:
					mrg2 = numbers[1]

		# start constructing a new cluster
		newClustNum = str(m + len(Z))
		newClust = clusters.pop(str(mrg1))
		newClust.extend(clusters.pop(str(mrg2)))
		clusters[newClustNum] = newClust

		# update the distances
		dists = update_dist(mrg1, mrg2, clusters, dists, newClustNum, newClust)

		# add the cluster to Z
		Z.append([mrg1, mrg2, minDist, len(newClust)])

	# finally convert to a numPy array
	Z = np.array(Z)
	return Z

	
def euclidean_dist(data1, data2):
	distance = (data1[0] - data2[0]) ** 2
	distance += (data1[1] - data2[1]) ** 2
	return math.sqrt(distance)

def update_dist(mrg1, mrg2, clusters, dist, newClustNum, newClust):
	distCpy = dist.copy()

	# Rid all of the distances that had the cluster indexes that were merged
	for key, value in dist.items():
		keyVals = key.replace(':', ' ')
		keyNums = [int(s) for s in keyVals.split() if s.isdigit()]
		if mrg1 in keyNums:
			distCpy.pop(key)
		elif mrg2 in keyNums:
			distCpy.pop(key)

	# add the updated distances with the new cluster
	for clustNum1, clustVal1 in clusters.items():
		minVal = 99999999
		for vals1 in clustVal1:
			for vals2 in newClust:
				if clustNum1 == newClustNum: continue
				val = euclidean_dist(vals1, vals2)
				if val < minVal:
					minVal = val

		distCpy[clustNum1 + ':' + newClustNum] = minVal

	return distCpy

# takes in the number of samples we want to randomly generate, returns
# them in a single structure
def random_x_y(m):
	randData = []
	for i in range(m):
		randData.append((random.randint(1, 359), random.randint(1, 359)))

	return randData
	

# performs single linkage hierarchical agglomerative clustering on the 
# Pokemon with the x,y feature representation, and imshow the clustering
def imshow_hac(dataset):	
	m = len(dataset)
	clusters = {}
	dists = {}
	Z = []
	dataset = [dataset[i] for i in range(m) if np.all(np.isfinite(dataset[i]))]
	m = len(dataset)


	# plot
	plt.scatter([x[0] for x in dataset], [x[1] for x in dataset])


	# put all the data into a dict in the form [clustNum: [(x,y)]]
	for i in range(0, m):
		clustNum = str(i)
		clusters[clustNum] = [dataset[i]]

	# store original distances in the form ['clustNum1:clustNum2': dist]
	# this will help us later
	for clustNum1, clustVal1 in clusters.items():
		for clustNum2, clustVal2 in clusters.items():
			# skip ahead if we are comparing the same cluster
			if clustNum1 == clustNum2: continue
			dists[clustNum1 + ':' + clustNum2] = euclidean_dist(clustVal1[0], clustVal2[0])

	while len(clusters) > 1:

		minDist = min(dists.values())
		closestClusterNums = [key for key in dists if dists[key] == minDist]
		
		# some arbitrarily large number we can use to help with tie breaking
		mrg1 = mrg2 = 99999999

		# tie breakers
		for smallest in closestClusterNums:
			smallest = smallest.replace(':', ' ')
			numbers = [int(s) for s in smallest.split() if s.isdigit()]
			if numbers[0] <= mrg1:
				mrg1 = numbers[0]
				if numbers[1] < mrg2:
					mrg2 = numbers[1]

		# start constructing a new cluster
		newClustNum = str(m + len(Z))
		newClust = clusters.pop(str(mrg1))
		newClust.extend(clusters.pop(str(mrg2)))
		clusters[newClustNum] = newClust

		# update the distances
		dists = update_dist(mrg1, mrg2, clusters, dists, newClustNum, newClust)

		# add the cluster to Z
		Z.append([mrg1, mrg2, minDist, len(newClust)])

	# finally convert to a numPy array
	Z = np.array(Z)
	return Z
