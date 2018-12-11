import os 
import configparser
import math
import numpy as np
import json

class VAFile(object):
	"""Main class of VA-File."""

	def __init__(self, base_path, num_dim, num_points, num_bit, data_range=(0,1)):

		self.base_path = base_path
		self.num_dim = num_dim
		self.num_points = num_points
		self.num_bit = num_bit
		self.data_range = data_range
		b = self.num_bit % self.num_dim
		self.bjs = []
		for j in range(self.num_dim):
			if idx<=b:
				bj = b + 1
			else:
				bj = b
			self.bjs.append(bj)
		self.partitions = []
		self.boxes = {}

	def load_file(self, data_path):

		return True

	def bulk_load(self, bulk_data):

		histograms = []
		volume = 10
		for j,bj in enumerate(self.bjs):
			partition = [0]
			histogram = []
			num_bins = int(pow(2,bj)*volume)
			for i in range(num_bins):
				histogram.append(0)
			self.partitions.append(partition)
			histograms.append(histogram)

		for n, data_tuple in enumerate(bulk_data):
			for d, data in enumerate(data_tuple):
				bj = bjs[d]
				num_bins = int(pow(2,bj)*volume)
				edge = int(math.floor(data*num_bins))
				histograms[d][edge] += 1

		for j,bj in enumerate(self.bjs):
			partition = self.partitions[j]
			size = 1./pow(2,bj)
			num_bins = int(pow(2,bj)*volume)
			sum_bins = 0
			for i in range(num_bins):
				sum_bins += histograms[j][i]
				if sum_bins > size*self.num_points:
					partition.append(1.*(i-1)/num_bins)
					sum_bins = histograms[j][i]
			partition.append(1)

		for data_tuple in bulk_data:
			if not check_valid(data_tuple):
				return False
			appro_list = approximate(self, data_tuple)
			seperator = ''
			appro = seperator.join(appro_list)
			if appro not in self.boxes:
				self.boxes[appro] = []
			box =  self.boxes[appro]
			box.append(data_tuple)

		return True

	# def insert_tuple(self, data_tuple):

	# 	return True;

	# def delete_tuple(self, data_tuple):

	# 	return True;

	# def update_file(self):

	# 	return True

	def check_valid(self, data_tuple):

		if isinstance(data_tuple, tuple):
			return False
		elif len(tuple) is not self.num_dim:
			return False
		for data in data_tuple:
			if data<self.data_range[0] or data>self.data_range[1]:
				return False
		return True

	def approximate(self, data_tuple):

		if not check_valid(data_tuple)
			return False
		appro_list = []
		for idx, data in enumerate(data_tuple):
			marks = self.partitions[idx]
			bj = self.bjs[idx]
			left = 0
			right = len(marks)-1
			while left<right:
				mid = left + (right-left)//2
				if marks[mid]<=data and data<marks[mid+1]:
					appro_list.append(dim_appro(mid,bj))
				elif marks[mid]<data:
					left = mid + 1
				elif:
					right = mid

		return appro_list

	def dim_appro(self, mark, bj):

		binary_data = format(mark, '0' + str(bj) + 'b')
		return binary_data

	def nearest_search(self, pivot_tuple, num_nearest):

		tuple_list = []
		if not check_valid(pivot_tuple):
			return tuple_list

		return tuple_list

	def lower_bound(self, pivot_tuple):

		lb = {}
		for box in self.boxes:
			element = []
			for i in range(self.num_dim):
				rij = int(box, 2)
				marks = partitions[i]
				if rqj>rij:
					diff = qj - marks[rij+1]
				elif rqj==rij:
					diff = 0
				elif rqj<rij:
					diff = marks[rij]-qj
				w_diff = weights[i] * diff
				element.append(w_diff, p)
			dist = pow(sum(element),1./p)
			lb['box'] = dist

		return lb

	def upper_bound(self, pivot_tuple):

		ub = {}
		for box in self.boxes:
			element = []
			for i in range(self.num_dim):
				rij = int(box, 2)
				marks = partitions[i]
				if rqj>rij:
					diff = qj - marks[rij]
				elif rqj==rij:
					diff = max(qj - marks[rij], marks[rij+1]-qj)
				elif rqj<rij:
					diff = marks[rij+1]-qj
				diff = abs(pivot_tuple[i] - data_tuple[i])
				w_diff = weights[i] * diff
				element.append(w_diff, p)
			dist = pow(sum(element),1./p)
			ub['box'] = dist

		return ub

	def distance(self, p, pivot_tuple, data_tuple, weights=None):

		if not check_valid(pivot_tuple)
			return False
		if not check_valid(data_tuple)
			return False

		if weights is None:
			weights = [1] * length
		if len(weights) is not self.num_dim:
			return False

		element = []
		for i in range(self.num_dim):
			diff = abs(pivot_tuple[i] - data_tuple[i])
			w_diff = weights[i] * diff
			element.append(w_diff, p)
		dist = pow(sum(element),1./p)

		return dist

