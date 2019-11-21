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
	class Tree(object):
		def __init__(self,attr):
			self.attr = attr
			self.parent = None
			self.branches = {}
		def addBranch(self,key,branch):
			self.branches[key] = branch
			if type(branch) == type(self):
				self.branches[key].parent = self
		def __str__(self):
			str1 = ""
			if self.parent != None:
				str1 += str(self.parent.attr)+" --> "+str(self.attr)
			else:
				str1 += str(self.attr)
			for b in self.branches:
				if type(self.branches[b]) == type(self):
					str1 += "\n\tbranch: "+str(b)+"\tattr: "+str(self.branches[b].attr)
				else:
					str1 += "\n\tbranch: "+str(b)+"\tout: "+str(self.branches[b])
			return str1

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
		norm_data = np.clip((data - self.range[0]) / (self.range[1] - self.range[0]), 0, 1)
		categorical_data = np.floor(self.bin_size*norm_data).astype(int)
		return categorical_data

	def train(self, X, y):
		#training logic here
		#input is array of features and labels
		categorical_data = self.preprocess(X)
		attributes = np.arange(np.size(categorical_data,1))
		examples = []
		for d in range(len(categorical_data)):
			n_example = self.Node(d,categorical_data[d],y[d])
			examples.append(n_example)
		self.tree = self.treebuilding(examples,attributes,None)

	def treebuilding(self,examples,attributes,parent_examples):
		if examples == None:
			return self.plurality_value(parent_examples)
		elif self.isSameLabel(examples):
			return examples[-1].value
		elif len(attributes)==0:
			return self.plurality_value(examples)
		else:
			target_attr = self.getBestAttribute(examples,attributes)
			new_attr = attributes[attributes!=target_attr]
			n_tree = self.Tree(target_attr)
			
			for v in self.getValuesWithAttribute(target_attr,examples):
				n_example = self.getExamplesWithAttributeValue(examples,target_attr,v)
				subtree = self.treebuilding(n_example,new_attr,examples)
				# print(subtree)
				n_tree.addBranch(v,subtree)
			# print(n_tree)
		return n_tree

	def getExamplesWithAttributeValue(self,examples,attr,v):
		n_example = []
		for ex in examples:
			if ex.data[attr] == v:
				n_example.append(ex)
		return n_example

	def getValuesWithAttribute(self,attr,examples):
		# print("getValuesWithAttribute",attr)
		totalExample = len(examples)
		values = {}
		for ex in examples:
			if ex.data[attr] not in values:
				values[ex.data[attr]] = [ex]
			else:
				values[ex.data[attr]].append(ex)
		return values

	def infoCompute(self,p_value,n_value):
		# print("infoCompute")
		ans = 0
		total = p_value + n_value
		if total != 0:
			p_d = p_value/total
			n_d = n_value/total
			if p_d != 0:
				ans = -(p_d)*np.log2(p_d)
			if n_d != 0:
				ans = -(n_d)*np.log2(n_d)
		return ans

	def getPNValue(self,examples):
		# print("getPNValue")
		exP = exN = 0
		for ex in examples:
			if ex.value == 1:
				exP +=1
			else:
				exN +=1
		return exP,exN

	def sumOfInformation(self,examples,attr):
		# print("sumOfInformation")
		totalExample = len(examples)
		values = self.getValuesWithAttribute(attr,examples)
		currentTotal = 0
		for v in values:
			vP,vN = self.getPNValue(values[v])
			# print("vP,vN",vP,vN)
			currentTotal += vP/totalExample*self.infoCompute(vP,vN)
		return currentTotal

	def gain(self,attr,examples):
		# print("in gain, attr = ",attr)
		exP,exN = self.getPNValue(examples)
		expectedInfo = self.infoCompute(exP,exN)
		infomationNeeded = self.sumOfInformation(examples,attr)
		ans = expectedInfo - infomationNeeded
		# print("\tgain:",ans)
		return ans

	def getBestAttribute(self,examples,attributes):
		# print("in getBestAttribute")
		best_Attribute = None
		for attr in attributes:
			current_gain = self.gain(attr,examples)
			if best_Attribute == None or current_gain > best_Attribute[1]:
				best_Attribute = (attr,current_gain)
		return best_Attribute[0]

	def isSameLabel(self,examples):
		# print("is same label")
		isSame = True
		lastValue = examples[0].value
		for ex in examples:
			if ex.value != lastValue:
				isSame = False
				break
		return isSame

	def plurality_value(self,examples):
		# print("in plurality_value")
		major = {}
		for ex in examples:
			option = ex.value
			if option not in major:
				major[option] = 1
			else:
				major[option] += 1
		res = max(major,key=lambda k:major[k])
		# print("plurality_value",res)
		return res

	def printTree(self,t):
		print(t)
		for b in t.branches:
			if type(t.branches[b]) == type(t):
				self.printTree(t.branches[b])
		return None

	def readData(self,t,data):
		data_v = data[t.attr]
		if not data_v in t.branches:
			return self.getMajorityOutcome(t) #need to get majority outcome
		n_t = t.branches[data_v]
		if type(n_t) == type(t):
			return self.readData(n_t,data)
		else:
			return n_t

	def getOutcome(self,t):
		outcome = []
		for b in t.branches:
			c_branch = t.branches[b]
			if type(c_branch) == type(self.tree):
				_out = self.getOutcome(c_branch)
				outcome += _out
			else:
				outcome.append(c_branch)
		
		return outcome

	def getMajorityOutcome(self,t):
		outcome = self.getOutcome(t)
		Ans0 = Ans1 = 0
		for out in outcome:
			if out == 0:
				Ans0 += 1
			else:
				Ans1 += 1
		if Ans1 > Ans0:
			return 1
		elif Ans0 < Ans1:
			return 0
		else:
			return np.random.randint(0,1)

	def predict(self, X):
		#Run model here
		#Return array of predictions where there is one prediction for each set of features
		categorical_data = self.preprocess(X)
		prediction = np.array([])
		# self.printTree(self.tree) #for debugging
		for row in categorical_data:
			# print("------------------------ROOT------------------------")
			prediction = np.append(prediction,self.readData(self.tree,row))
			# break #for debugging
		return prediction

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