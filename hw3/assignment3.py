import numpy as np

class KNN:
	def __init__(self, k):
		#KNN state here
		#Feel free to add methods
		self.k = k

	def distance(self, x1, x2):
		diffs = (x1 - x2)**2
		if(x1.ndim == 1):
			return np.sqrt(diffs.sum())
		return np.sqrt(diffs.sum(1))

	def train(self, X, y):
		#training logic here
		#input is an array of features and labels
		self.features = X
		self.labels = y
		# print("features",self.features,"how long?",len(self.features))
		# print("labels",self.labels,"how long?",len(self.labels)) 
		return None

	def findNeighbors(self,target):
		distance = []
		for f in range(len(self.features)):
			dist = self.distance(target,self.features[f])
			label = self.labels[f]
			distance.append([label,dist])
		distance.sort(key=lambda x:x[1])
		neighbors = distance[:self.k]
		return neighbors

	def findMajority(self,neighbors):
		major = {}
		for n in range(len(neighbors)):
			option = neighbors[n][0]
			if option not in major:
				major[option] = 1
			else:
				major[option] += 1
		res = max(major,key=lambda k:major[k])
		return res

	def predict(self, X):
		#Run model here
		#Return array of predictions where there is one prediction for each set of features
		result = []
		for x in X:
			neighbors = self.findNeighbors(x)
			outcome = self.findMajority(neighbors)
			result.append(outcome)
		return np.ravel(result)

class ID3:
	def __init__(self, nbins, data_range):
		#Decision tree state here
		#Feel free to add methods
		self.bin_size = nbins
		self.range = data_range

	def preprocess(self, data):
		#Our dataset only has continuous data
		norm_data = (data - self.range[0]) / np.maximum((self.range[1] - self.range[0]), 1e-6)
		categorical_data = np.floor(self.bin_size*norm_data).astype(int)
		return np.clip(categorical_data, 0, self.bin_size - 1)

	def train(self, X, y):
		#training logic here
		#input is array of features and labels
		categorical_data = self.preprocess(X)

	def predict(self, X):
		#Run model here
		#Return array of predictions where there is one prediction for each set of features
		categorical_data = self.preprocess(X)
		return None

class Perceptron:
	def __init__(self, w, b, lr):
		#Perceptron state here, input initial weight matrix
		#Feel free to add methods
		self.lr = lr
		self.w = w
		self.b = b

	def train(self, X, y, steps):
		#training logic here
		#input is array of features and labels
		None

	def predict(self, X):
		#Run model here
		#Return array of predictions where there is one prediction for each set of features
		return None

class MLP:
	def __init__(self, w1, b1, w2, b2, lr):
		self.l1 = FCLayer(w1, b1, lr)
		self.a1 = Sigmoid()
		self.l2 = FCLayer(w2, b2, lr)
		self.a2 = Sigmoid()

	def MSE(self, prediction, target):
		return np.square(target - prediction).sum()
		

	def MSEGrad(self, prediction, target):
		return - 2.0 * (target - prediction)
		

	def shuffle(self, X, y):
		idxs = np.arange(y.size)
		np.random.shuffle(idxs)
		return X[idxs], y[idxs]
		

	def train(self, X, y, steps):
		for s in range(steps):
			i = s % y.size
			if(i == 0):
				X, y = self.shuffle(X,y)
			xi = np.expand_dims(X[i], axis=0)
			yi = np.expand_dims(y[i], axis=0)

			pred = self.l1.forward(xi)
			pred = self.a1.forward(pred)
			pred = self.l2.forward(pred)
			pred = self.a2.forward(pred)
			loss = self.MSE(pred, yi) 
			#print(loss)

			grad = self.MSEGrad(pred, yi)
			grad = self.a2.backward(grad)
			grad = self.l2.backward(grad)
			grad = self.a1.backward(grad)
			grad = self.l1.backward(grad)
		None

	def predict(self, X):
		pred = self.l1.forward(X)
		pred = self.a1.forward(pred)
		pred = self.l2.forward(pred)
		pred = self.a2.forward(pred)
		pred = np.round(pred)
		return np.ravel(pred)

class FCLayer:

	def __init__(self, w, b, lr):
		self.lr = lr
		self.w = w	#Each column represents all the weights going into an output node
		self.b = b

	def forward(self, input):
		#Write forward pass here
		return None

	def backward(self, gradients):
		#Write backward pass here
		return None	

class Sigmoid:

	def __init__(self):
		None

	def forward(self, input):
		#Write forward pass here
		return None

	def backward(self, gradients):
		#Write backward pass here
		return None	