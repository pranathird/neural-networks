import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
import pymongo
from pymongo import MongoClient
import numpy as np

client = MongoClient('mongodb://localhost:27017/')
db = client['snp']
translationVariable = 90000000
windowLength = 500000000
count = 0 
snpcandle = ['1day','1hour','30mins','4hours']
snpIndex = [ snpcandle[0], snpcandle[1], snpcandle[2], snpcandle[3]]
lr = 0.001
training_iters = 100000
windowStart = 0
windowEnd = 0
n_inputs = 28   # MNIST data input (img shape: 28*28)
n_steps = 28	# time steps
n_hidden_units = 128   # neurons in hidden layer
n_classes = 10	  # MNIST classes (0-9 digits)
listofWindows={chartType:[] for i,chartType in enumerate(snpcandle)}
oneWindow = []
batch_size=10
loopOn = True


def my_func(arg):
	arg = tf.convert_to_tensor(arg, dtype = tf.float32)

	return arg

for i,chartType in enumerate(snpcandle):
	if chartType=='1day':
		start = db[chartType].find().sort([('epochDate',1)]).limit(1)
		end = db[chartType].find().sort([('epochDate',-1)]).limit(1)
		
		# print (start, end)

		for beginCandle in start:
			windowStart = beginCandle['epochDate']
			windowEnd = windowStart + windowLength

		for lastCandle in end:
			lastTimeStamp = lastCandle['epochDate']
		
		while loopOn:
			oneWindow = []			
			windowStart = windowStart + translationVariable

			# windowEnd = windowEnd + translationVariable
			count = 0
			mongoOneWindow = db[chartType].find( {'epochDate' : { '$gt' :  windowStart}}).limit(10)
			for val in mongoOneWindow:count +=1

			if count == 10:
				loopOn = True
			else:
				loopOn = False

			for candle in mongoOneWindow:
				# print(type(candle['_id']))
				candleIteration = []
				for k,v in candle.items():
					if k=='Open' or k=='High' or  k=='Low' or k=='Open' or k=='Close' or k=='Volume' or k=='epochDate':
						candleIteration.append(v)
				# print(len(candleIteration))
				oneWindow.append(candleIteration)
			listofWindows[chartType].append(my_func(oneWindow)) 

	# print(listofWindows[chartType])
print(tf.shape(listofWindows['1day']))
			# we don't pass listofWindows[chartType] to my_func

with tf.Session() as sess:

	sess.run(tf.global_variables_initializer())



# print('batches and global initialization imported')
