from misc import *
import random

def genetic_linear(points):
	repeats, upd_period, CR, F = 1, 200, 0.9, 0.8
	dim = len(points[0])
	generation_size = dim * 10
	random.seed(960172)

	def get_event(prob):
		return random.random() < prob
	def get_mutant(a, b, c):
		ret = a.copy()
		for i in range(dim):
			ret[i] += F * (b[i] - c[i])
		return ret
	def crossover(a, b):
		ret = a.copy()
		for i in range(dim):
			if not get_event(CR):
				ret[i] = b[i]
		return ret

	best_result = [Linear(0, 0, 0), Linear(0, 0, 0).std(points)]
	def update(inst, value):
		if value < best_result[1]:
			best_result[0] = Linear(inst[0], inst[1], inst[2])
			best_result[1] = value

	for rep in range(repeats):
		eprint("Start %d repeat" % (rep + 1))
		generation = [[random.uniform(0, 100000) for _ in range(dim)] for _ in range(generation_size)]
		values = list(map(lambda x: Linear(x[0], x[1], x[2]).std(points), generation))
		for iter in range(upd_period):
			new_generation, new_values = [], []
			for i in range(generation_size):
				v1, v2, v3 = [-1] * 3
				while v1 == v2 or v2 == v3 or v3 == v1 or i in (v1, v2, v3):
					v1, v2, v3 = [random.randint(0, generation_size - 1) for _ in range(3)]
				v = crossover(get_mutant(generation[v1], generation[v2], generation[v3]), generation[i])
				vval = Linear(v[0], v[1], v[2]).std(points)
				if vval < values[i]:
					new_generation.append(v)
					new_values.append(vval)
				else:
					new_generation.append(generation[i])
					new_values.append(values[i])
			generation, values = new_generation, new_values
		for i in range(generation_size):
			update(generation[i], values[i])

	return best_result[0]