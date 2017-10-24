from misc import Linear
import numpy as np
from time import time

def fair_linear(points):
	starttime = time()
	F = np.matrix([[p[0], p[1], 1.0] for p in points])
	Ft = F.getT()
	Fp = np.linalg.inv(Ft * F) * Ft
	Astar = Fp * np.matrix([[p[2]] for p in points])
	linear = Linear(float(Astar[0][0]), float(Astar[1][0]), float(Astar[2][0]))
	return ([(linear.std(points), time() - starttime)], 'r'), linear
