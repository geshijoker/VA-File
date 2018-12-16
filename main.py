import os 
import configparser
import math
import json
import random
import pickle

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR,'data/')
print('BASE_DIR: ' + BASE_DIR)
print('DATA_DIR: ' + DATA_DIR)

data = []
for i in range(500000):
	temp = []
	for j in range(20):
		temp.append(random.uniform(0, 1))
	data.append(temp)

pickle.dump(data,open("./500000_20.p","wb"))

