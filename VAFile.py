import os 
import configparser
import math
import numpy as np
import heapq
import json

class VAFile(object):
	"""Main class of VA-File."""

	def __init__(self, base_path, num_dim, num_points, num_bit, data_range=(0,1)):
		"""
        Constructor

        :param base_path: the base path of the repo
        :param num_dim: the number of dimensions of the data
        :param num_points: the number of data points
        :param num_bit: the number of bits for an approximation
        :param data_range: the range of data in each dimension, default (0,1)
        """
		self.base_path = base_path
		self.num_dim = num_dim
		self.num_points = num_points
		self.num_bit = num_bit
		self.data_range = data_range
		b = self.num_bit % self.num_dim
		l = self.num_bit // self.num_dim
		self.cands = []
		self.bjs = []
		# distribute bits to different dimensions
		for j in range(self.num_dim):
			if j<b:
				bj = l + 1
			else:
				bj = l
			self.bjs.append(bj)
		self.partitions = []
		self.boxes = {}

	def bulk_load(self, bulk_data):
		"""
        load a bulk of data

        :param bulk_data: a bulk of data -- a list of list of size (num_points, num_dim)
        """
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

		for j,bj in enumerate(self.bjs):
			size = pow(2,bj)
			div = int(1.*len(bulk_data)/size)
			partition = self.partitions[j]
			s = sorted(bulk_data, key=lambda x: x[j])
			for i in range(size-1):
				partition.append(s[(i+1)*div][j])
			partition.append(1)

		for data_tuple in bulk_data:
			if not self.check_valid(data_tuple):
				return False
			appro_list = self.approximate(data_tuple)
			seperator = ''
			appro = seperator.join(appro_list)
			if appro not in self.boxes:
				self.boxes[appro] = []
			box =  self.boxes[appro]
			box.append(data_tuple)

		return len(self.boxes)

	def check_valid(self, data_tuple):
		"""
        check the data point is valid with the size and range

        :param data_tuple: a data point -- size (num_dim), range
        """
		if isinstance(data_tuple, tuple):
			return False
		elif len(data_tuple) is not self.num_dim:
			return False
		for data in data_tuple:
			if data<self.data_range[0] or data>self.data_range[1]:
				return False
		return True

	def approximate(self, data_tuple):
		"""
        assign each data point with an approximation

        :param data_tuple: a data point
        """
		if not self.check_valid(data_tuple):
			return False
		appro_list = []
		for idx, data in enumerate(data_tuple):
			marks = self.partitions[idx]
			bj = self.bjs[idx]

			for i in range(1,len(marks)):
				if data<=marks[i]:
					appro_list.append(self.dim_appro(i-1,bj))
					break

		return appro_list

	def dim_appro(self, mark, bj):
		"""
        binary approximate of one mark in the j_th dimension

        :param mark: the approximated mark of a data point in j_th dimension
        :param bj: number of bits in the j_th dimension to keep the format valid
        """
		binary_data = format(mark, '0' + str(bj) + 'b')
		return binary_data

	def nearest_search(self, p, pivot_tuple, num_nearest):
		"""
        binary approximate of one mark in the j_th dimension

        :param p: p order when computing distances
        :param pivot_tuple: the anchor point which you are finding the nearest point with
        :param num_nearest: the number of nearest data points to the anchor point
        """
		if not self.check_valid(pivot_tuple):
			return False
		k = num_nearest

		delta,_ = self.init_candidate(k,(self.num_dim)^2)
		hp = []
		heapq.heapify(hp)
		lb, ub = self.get_bounds(p, pivot_tuple)
		count = 0
		for box in self.boxes:
			li = lb[box]
			ui = ub[box]
			if li <= delta:
				delta,_ = self.candidate(ui, box)
#				if ui <= delta:
				heapq.heappush(hp, (li,box))

		count = 0
		delta,_ = self.init_candidate(k,delta)
		li, box = heapq.heappop(hp)
		while li<delta:
			for data_tuple in self.boxes[box]:
				count += 1
				delta,_ = self.candidate(self.distance(p, pivot_tuple, data_tuple), data_tuple)
			if len(hp)==0:
				break
			li, box = heapq.heappop(hp)
		return self.cands, count

	def init_candidate(self, size, value):
		"""
        initial the candidate array of a given size with the value

        :param size: the size of the candidate array
        :param value: the value for initialization

        :return: the initialized value after initialization
        """
		self.cands.clear()
		for i in range(size):
			self.cands.append((value,[]))

		return self.cands[-1]

	def candidate(self, dist, entry):
		"""
        check the if the entry is a valid candidate, sort the candidates and return the furthest one

        :param dist: the distance of the entry to the anchor point
        :param entry: the element whose distance to the anchor point is known, can be another data point or a box

        :return the updated furthest candidate
        """
		if dist>=self.cands[-1][0]:
			return self.cands[-1]

		for i in range(len(self.cands)):
			if self.cands[i][0]>dist:
				break
		found = i

		for i in range(len(self.cands)-1, found, -1):
			self.cands[i] = self.cands[i-1]
		self.cands[found] = (dist, entry)

		return self.cands[-1]


	def get_bounds(self, p, pivot_tuple, weights=None):
		"""
        get the the upper and lower bounds of the distances of all boxes to the anchor data point

		:param p: p order when computing distances
        :param pivot_tuple: the anchor data point
        :param weights: assigned weights of dimensions, default all 1s
        """
		lb = self.lower_bound(p, pivot_tuple, weights=None)
		ub = self.upper_bound(p, pivot_tuple, weights=None)

		return lb, ub

	def lower_bound(self, p, pivot_tuple, weights=None):
		"""
        compute the lower bounds of the distances of all boxes to the anchor data point

		:param p: p order when computing distances
        :param pivot_tuple: the anchor data point
        :param weights: assigned weights of dimensions, default all 1s
        """
		if weights is None:
			weights = [1] * self.num_dim
		if len(weights) is not self.num_dim:
			return False

		appro_pivot = self.approximate(pivot_tuple)
		lb = {}
		for box in self.boxes:
			element = []
			for i in range(self.num_dim):
				index = sum(self.bjs[:i])
				dim_box = box[index:index+self.bjs[i]]
				rij = int(dim_box, 2)
				pivot_box = appro_pivot[i]
				rqj = int(pivot_box, 2)
				qj = pivot_tuple[i]
				marks = self.partitions[i]
				if rqj>rij:
					diff = qj - marks[rij+1]
				elif rqj==rij:
					diff = 0
				elif rqj<rij:
					diff = marks[rij] - qj
				w_diff = weights[i] * diff
				element.append(pow(w_diff,p))
			dist = pow(sum(element),1./p)
			lb[box] = dist

		return lb

	def upper_bound(self, p, pivot_tuple, weights=None):
		"""
        compute the upper bounds of the distances of all boxes to the anchor data point

		:param p: p order when computing distances
        :param pivot_tuple: the anchor data point
        :param weights: assigned weights of dimensions, default all 1s
        """
		if weights is None:
			weights = [1] * self.num_dim
		if len(weights) is not self.num_dim:
			return False

		appro_pivot = self.approximate(pivot_tuple)
		ub = {}
		for box in self.boxes:
			element = []
			for i in range(self.num_dim):
				index = sum(self.bjs[:i])
				dim_box = box[index:index+self.bjs[i]]
				rij = int(dim_box, 2)
				pivot_box = appro_pivot[i]
				rqj = int(pivot_box, 2)
				qj = pivot_tuple[i]
				marks = self.partitions[i]
				if rqj>rij:
					diff = qj - marks[rij]
				elif rqj==rij:
					diff = max(qj - marks[rij], marks[rij+1]-qj)
				elif rqj<rij:
					diff = marks[rij+1]-qj
				w_diff = weights[i] * diff
				element.append(pow(w_diff,p))
			dist = pow(sum(element),1./p)
			ub[box] = dist

		return ub

	def distance(self, p, pivot_tuple, data_tuple, weights=None):
		"""
        compute the p order distance between two data points

		:param p: p order when computing distances
        :param pivot_tuple: the anchor data point
        :param data_tuple: the target data point
        :param weights: assigned weights of dimensions, default all 1s
        """
		if not self.check_valid(pivot_tuple):
			return False
		if not self.check_valid(data_tuple):
			return False

		if weights is None:
			weights = [1] * self.num_dim
		if len(weights) is not self.num_dim:
			return False

		element = []
		for i in range(self.num_dim):
			diff = abs(pivot_tuple[i] - data_tuple[i])
			w_diff = weights[i] * diff
			element.append(pow(w_diff,p))
		dist = pow(sum(element),1./p)

		return dist

