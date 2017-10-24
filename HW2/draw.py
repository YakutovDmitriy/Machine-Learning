'''
Demonstrates plotting a 3D surface colored with the coolwarm color map.
The surface is made opaque by using antialiased=False.

Also demonstrates using the LinearLocator and custom formatting for the
z axis tick labels.
'''
from misc import *
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

def draw(xs, ys, zs, linear):
	eprint("Start draw")
	eprint.enter()
	fig = plt.figure()
	ax = fig.gca(projection='3d')

	def make_range(xs):
		mean = (min(xs) + max(xs)) / 2
		rad = 1.2 * (max(xs) - mean)
		return np.arange(mean - rad, mean + rad, rad / 50)

	X, Y = np.meshgrid(*map(make_range, [xs, ys]))
	Z = [[0] * X.shape[1] for _ in range(X.shape[0])]
	for i in range(len(Z)):
		for j in range(len(Z[i])):
			Z[i][j] = linear(float(X[i][j]), float(Y[i][j]))
	Z = np.array(Z)
	surf = ax.plot_surface(X, Y, Z, cmap='coolwarm',
	                       linewidth=0, antialiased=True)

	# Customize the z axis.
	zmean = (max(zs) + min(zs)) / 2.0
	zrad = 3 * (max(zs) - zmean)
	ax.set_zlim(zmean - zrad, zmean + zrad)
	ax.zaxis.set_major_locator(LinearLocator(10))
	ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
	ax.xaxis.set_label('area')
	ax.yaxis.set_label('rooms')
	ax.zaxis.set_label('price')

	for x, y, z in zip(xs, ys, zs):
		ax.scatter(x, y, z, c='b', marker='o')

	fig.colorbar(surf, shrink=0.5, aspect=5)
	plt.show()
	eprint.exit()

def build_graph(graphs):
	cmap_bold = ListedColormap(['#000000', '#ffffff'])
	plt.figure()
	plt.rcParams["figure.figsize"] = list(map(lambda x: x * 1, plt.rcParams["figure.figsize"]))
	for i, graph in enumerate(graphs):
		graph, color = graph[0], graph[1]
		yy, xx = map(list, zip(*graph))
		plt.scatter(xx, yy,  c=color,cmap=cmap_bold,linewidths=0, s = 5 - i)
	plt.xlim(0, 2)
	plt.ylim(0, 4 * 10 ** 5)
	plt.title("Time all")
	plt.show()
