from misc import *
import random

def descent_linear(points):
	np.random.seed(2018)
	# this method will change w
	def learningRate(w, n, x, y):
		print(w, x, y)
		for i in range(0, w.shape[0]):
			w[i] = w[i] - n * 2 * (1 - w[i] * x[i] * y) * (-x[i] * y)


	def getStartPoint(points, answers):
		w = np.copy(points[0])
		n = points.shape[1]
		for i in range(points.shape[1]):
			w[i] = np.random.uniform( -1/ (2 * n), 1 / (2 * n))
		return w
	points = np.array(points)
	np.random.shuffle(points)
	y = points[:, 2]
	x = np.array([[p[0], p[1], 1.0] for p in points])

	w = getStartPoint(x, y)

	def lossFunction(w, x, y):
		return (1 - (np.dot(x, w)) * y) ** 2

	def calcQ(w, points, answers):
		q = 0
		for i in range(0, points.shape[0]):
			q += lossFunction(w, points[i], answers[i]) 
		return q

	curQ = calcQ(w, x, y)
	_lambda = 1 / points.shape[0]
	for iter in range(100):
		curIndex = np.random.randint(0, x.shape[0] - 1)
		curX = x[curIndex]
		curY = y[curIndex]
		curEps = lossFunction(w, curX, curY)
		w0 = np.copy(w)
		learningRate(w, 0.005, curX, curY)
		#prevQ = curQ
		#curQ = calcQ(w, x, y)


	return Linear(w[0], w[1], w[2])

data = read_csv("prices_all.csv")[1:]
for i in range(len(data)):
	for j in range(len(data[i])):
		data[i][j] = float(data[i][j])
descent_linear(data)
