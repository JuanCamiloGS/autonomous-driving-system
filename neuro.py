import numpy as np
from keras.models import Sequential,Model
from keras.layers import Dense, Lambda,merge,Input
from keras.models import model_from_json
import timeit

class Neuro(object):

	def __init__(self):

		t_ans = raw_input("Desea entrenar la red: 0 (No) 1 (Si) ")

		while(not (t_ans in ['0','1'])):
			print ('Error, valor no permitido')
			t_ans = raw_input("Desea entrenar la red: 0 (No) 1 (Si) ") 
			print t_ans
   
		if t_ans == '1':
			#Training
			# fix random seed for reproducibility
			np.random.seed(128)
			steerds = np.loadtxt("Datasets/Dataset_training_steer_opponents_offsetFIVEB.csv", delimiter=",")
			# split into input (X) and output (Y) variables

			X3= steerds[:,0:7]
			Y3 = steerds[:,7:9]
            		Y3[:,0] = np.add(Y3[:,0],Y3[:,1])
			# Create model
			model = Sequential()
			model.add(Dense(7, input_dim=7, activation='relu',kernel_initializer="uniform"))
			model.add(Dense(76, activation='relu'))
			model.add(Dense(48, activation='relu'))
			model.add(Dense(1,activation='linear'))

			# Compile model
			model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])

			# Fit the model
			print("Starting fitting.....")

			model.fit(X3[:,0:7], Y3[:,0], epochs=200, batch_size=128)
			# evaluate the model
			print("Done....")
			print("Starting evaluation.....")
			scores = model.evaluate(X3[:,0:7], Y3[:,0])
			print("%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))
			print("Done")
			# serialize model to JSON
			model_json = model.to_json()
			with open("model2.json", "w") as json_file:
				json_file.write(model_json)
				# serialize weights to HDF5
				model.save_weights("model2.h5")
				print("Saved model to disk")
			# load json and create model
			json_file = open('model2.json', 'r')
			loaded_model_json = json_file.read()
			json_file.close()
			self.loaded_model = model_from_json(loaded_model_json)
			# load weights into new model
			self.loaded_model.load_weights("model2.h5")
			print("Loaded model from disk")
			
		else:
			# load json and create model
			json_file = open('model2.json', 'r')
			loaded_model_json = json_file.read()
			json_file.close()
			self.loaded_model = model_from_json(loaded_model_json)
			# load weights into new model
			self.loaded_model.load_weights("model2.h5")
			print("Loaded model from disk")
		self.PredictSteer([0,0,0,0,0,0,0])

	def PredictSteer(self, P):
		P = np.array(P)
		P = P.reshape(1,7)
		predictions = self.loaded_model.predict(P)
		rounded = [x[0] for x in predictions][0]
		return predictions[0]

	
