import os 
import configparser
import math
import json
import random
import pickle
import time
import numpy as np
from VAFile import VAFile

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR,'data/')
print('BASE_DIR: ' + BASE_DIR)
print('DATA_DIR: ' + DATA_DIR)

f = open("13143_64.p",'rb')
images = pickle.load(f)
# uppder bound of dimension in experiments
D = 41
# number of split in every dimension
num_split = 8
# number of Monte Carlo experiments for any dimension d
test_num = 5

def make_synthetic_data(size, dim):
	data = []
	for i in range(size):
		temp = []
		for j in range(dim):
			temp.append(random.uniform(0, 1))
		data.append(temp)
	pickle.dump(data,open('../' + str(size) + '_' + str(dim) + '.p','wb'))

def generate_data(d, n):
	data = np.zeros(shape = [n,d])
	for i in range(d):
		dimension_i = np.random.uniform(0,1,n)
		data[:,i] = dimension_i
	return data

def generate_normal(d, n):
	data = np.zeros(shape = [n,d])
	for i in range(d):
		mu = np.random.random(1)
		dimension_i = np.random.normal(mu,1,n)
		dimension_i[dimension_i > 1] = 1
		dimension_i[dimension_i < 0] = 0
		data[:,i] = dimension_i
	return data


# test uniform distribution
# size = 50000
# elapsed_uniform_ave = np.zeros(D -3)
# percentage_uniform_ave = np.zeros(D -3)
# for k in range(test_num):
# 	elapsed_uniform = []
# 	percentage_uniform = []
# 	for i in range(3,D):
# 		data = list(generate_data(i, size))
# 		vafile = VAFile('./', i, len(data), i*2)
# 		total = vafile.bulk_load(data)
# 		total = size
# 		pivot_tuple = data[random.randrange(size)]
# 		pivot_tuple = [0.5]*i

# 		curTime = time.time()
# 		cands, visited = vafile.nearest_search(2, pivot_tuple, 10)
# 		elapsed_uniform.append(time.time()-curTime)

# 		print('dimension = ',i,'visited_percentage(non-empty)',visited/total)
# 		percentage_uniform.append(visited/total)

# 	elapsed_uniform_ave  = elapsed_uniform_ave + np.array(elapsed_uniform)/test_num
# 	percentage_uniform_ave  = percentage_uniform_ave + np.array(percentage_uniform)/test_num
# 	print()

# pickle.dump(percentage_uniform_ave, open( "p_uniform_13_40.p", "wb" ) )
# pickle.dump(elapsed_uniform_ave, open( "e_uniform_13_40.p", "wb" ) )
# In[4]:

# test normal distribution
size = 50000
elapsed_normal_ave = np.zeros(D -3)
percentage_normal_ave = np.zeros(D -3)
for k in range(test_num):
	percentage_normal = []
	elapsed_normal = []
	for i in range(3,D):
		data = list(generate_normal(i, size))
		vafile = VAFile('./', i, len(data), i*2)
		total = vafile.bulk_load(data)
		total = size
		pivot_tuple = data[random.randrange(size)]
#		pivot_tuple = [0.5]*i

		curTime = time.time()
		cands, visited = vafile.nearest_search(2, pivot_tuple, 10)
		elapsed_normal.append(time.time()-curTime)

		print('dimension = ',i,'visited_percentage(non-empty)',visited/total)
		percentage_normal.append(visited/total)

	elapsed_normal_ave  = elapsed_normal_ave + np.array(elapsed_normal)/test_num
	percentage_normal_ave  = percentage_normal_ave + np.array(percentage_normal)/test_num
	print()
pickle.dump(percentage_normal_ave, open( "p_normal_13_40.p", "wb" ) )
pickle.dump(elapsed_normal_ave, open( "e_normal_13_40.p", "wb" ) )
# In[5]:

# test image data
size = 13143
elapsed_real_ave = np.zeros(D -3)
percentage_real_ave = np.zeros(D -3)
for k in range(test_num):
	percentage_real = []
	elapsed_real = []
	for i in range(3,D):
		data = list(images[:,0:i])
		vafile = VAFile('./', i, len(data), i*2)
		total = vafile.bulk_load(data)
		total = size
		pivot_tuple = list(images[np.random.randint(images.shape[0]),:])[0:i]

		curTime = time.time()
		cands, visited = vafile.nearest_search(2, pivot_tuple, 10)
		elapsed_real.append(time.time()-curTime)

		print('dimension = ',i,'visited_percentage(non-empty)',visited/total)
		percentage_real.append(visited/total)

	elapsed_real_ave  = elapsed_real_ave + np.array(elapsed_real)/test_num
	percentage_real_ave  = percentage_real_ave + np.array(percentage_real)/test_num
	print()
pickle.dump(percentage_real_ave, open( "p_real_13_40.p", "wb" ) )
pickle.dump(elapsed_real_ave, open( "e_real_13_40.p", "wb" ) )

# pickle.dump(percentage_real_ave, open( "p_real_13_40.p", "wb" ) )
# pickle.dump(percentage_normal_ave, open( "p_normal_13_40.p", "wb" ) )
# pickle.dump(percentage_uniform_ave, open( "p_uniform_13_40.p", "wb" ) )
# pickle.dump(elapsed_real_ave, open( "e_real_13_40.p", "wb" ) )
# pickle.dump(elapsed_normal_ave, open( "e_normal_13_40.p", "wb" ) )
# pickle.dump(elapsed_uniform_ave, open( "e_uniform_13_40.p", "wb" ) )
