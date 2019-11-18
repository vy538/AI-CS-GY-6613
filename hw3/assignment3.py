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
	class Node(object):
		def __init__(self,id,data,value):
			self.id = id
			self.data = data
			self.value = value
		def __str__(self):
			str1 = "id: "+str(self.id)+"\tdata: "+str(self.data)+"\n\toutcome: "+str(self.value)
			return str1

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
		# print(categorical_data[0],len(categorical_data[0]))
		attributes = np.arange(np.size(categorical_data,1))
		# print(attributes)
		examples = []
		for d in range(len(categorical_data)):
			n_example = self.Node(d,categorical_data[d],y[d])
			examples.append(n_example)
		self.tree = self.treebuilding(examples,attributes,None)

	def treebuilding(self,examples,attributes,parent_examples):
		if len(examples)==0:
			return self.plurality_value(parent_examples)
		elif self.isSameLabel(attributes):
			return attributes[-1]
		elif len(attributes) == 0:
			return self.plurality_value(examples)
		else:
			print("in else")
			n_attribute = self.getBestAttribute(examples,attributes)
			n_tree = self.generateNewTree(n_attribute)
			for v in self.getValueWithAttribute(n_attribute):
				n_example = self.getExamplesWithAttributeValue(examples,v)
				subtree = self.treebuilding(n_example,None,examples)#need to replace none
				n_tree = self.addBranch(subtree,n_tree)
		return None

	def addBranch(self,subTree,mainTree):
		return None

	def getExamplesWithAttributeValue(self,examples,value):
		return None

	def getValueWithAttribute(self,attr):
		return None

	def generateNewTree(self,attr):
		return None

	def infoCompute(self,p_value,n_value):
		print("infoCompute")
		total = p_value + n_value
		ans = -(p_value/total)*np.log2(p_value/total)
		# print("\thalf",ans)
		ans = -(n_value/total)*np.log2(n_value/total)
		# print("\tans",ans,total)
		return ans

	def getPNValue(self,examples):
		print("getPNValue")
		exP = exN = 0
		for ex in examples:
			if ex.value == 1:
				exP +=1
			else:
				exN +=1
		return exP,exN

	def sumOfInformation(self,examples,attr):
		print("sumOfInformation")
		totalExample = len(examples)
		values = {}
		for ex in examples:
			if ex.data[attr] not in values:
				values[ex.data[attr]] = [ex]
			else:
				values[ex.data[attr]].append(ex)

		currentTotal = 0
		for v in values:
			vP,vN = self.getPNValue(values[v])
			currentTotal += vP/totalExample*self.infoCompute(vP,vN)
		return currentTotal

	def gain(self,attr,examples):
		print("in gain, attr = ",attr)
		exP,exN = self.getPNValue(examples)
		expectedInfo = self.infoCompute(exP,exN)
		infomationNeeded = self.sumOfInformation(examples,attr)
		ans = expectedInfo - infomationNeeded
		return ans

	def getBestAttribute(self,examples,attributes):
		print("in getBestAttribute")
		best_Attribute = []
		for attr in range(len(attributes)):
			current_gain = self.gain(attributes[attr],examples)
			best_Attribute.append(current_gain)
		res = np.argmax(best_Attribute)
		return res

	def isSameLabel(self,attrs):
		print("is same label",len(np.unique(attrs)) == 1)
		return len(np.unique(attrs)) == 1

	def plurality_value(self,data):
		print("in plurality_value")
		major = {}
		for n in range(len(data)):
			option = data[n].value
			if option not in major:
				major[option] = 1
			else:
				major[option] += 1
		res = max(major,key=lambda k:major[k])
		print("plurality_value",res)
		return res

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