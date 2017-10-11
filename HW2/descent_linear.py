from misc import *
import random

def descent_linear(points):
	np.random.seed(2018)

	def a(w, x):
		return np.dot(w, x)

	def learningRate(w, n, x, y):
		w0 = np.copy(w)
		for i in range(w.shape[0]):
			w_i = 0
			for j in range(x.shape[0]):
				w_i += (a(w, x[j]) - y[j]) * x[j][i]
			w0[i] = w[i] -  2 * n * (1 / x.shape[0]) * w_i
		return w0

	def learningRateS(w, n, x, y):
		return w - 2 * n * (a(x, w) - y) * x

	def getStartPoint(points, answers):
		w = np.copy(points[0])	
		n = points.shape[1]
		for i in range(points.shape[1]):
			w[i] = np.random.uniform( -1/ (2 * n), 1 / (2 * n))
		return w


	points = np.array(points)
	np.random.shuffle(points)
	y = points[:, 2]

	maxArray = [max(points[:, i]) for i in range(points.shape[1])]
	maxY = max(y)
	y = y / maxY
	
	x = np.array([[p[0] / maxArray[0], p[1] / maxArray[1], 1.0] for p in points])
	xTest = np.array([[p[0], p[1] , 1.0] for p in points])

	w = getStartPoint(x, y)

	def lossFunction(w, x, y):
		return (y - np.dot(x, w)) ** 2

	def calcQ(w, points, answers):
		q = 0
		for i in range(0, points.shape[0]):
			q += lossFunction(w, points[i], answers[i]) 
		return q

	curQ = calcQ(w, x, y)
	_lambda = 1 / x.shape[0]
	eps = 1e-10
	curStep = 0
	while True:
		curIndex = np.random.randint(0, x.shape[0] - 1)
		curX = x[curIndex]
		curY = y[curIndex]
		curEps = lossFunction(w, curX, curY)
		#uncomment line below to use full dataset for training
		newW = learningRate(w, 0.25, x, y)
		
		#newW = learningRateS(w, 0.25, curX, curY)

		newQ = (1 - _lambda) * curQ + _lambda * curEps
		if (abs(curQ - newQ) < eps) or (np.linalg.norm(w - newW) < eps):
			break

		curQ = newQ
		w = newW
		curStep += 1
		if (curStep % 1000 == 0):
			print("curStep %i" % curStep)

	w[0] = w[0] / maxArray[0] * maxY
	w[1] = w[1] / maxArray[1] * maxY
	w[2] = w[2] * maxY
	return Linear(w[0], w[1], w[2])

