from misc import *
import random

def new_descent_linear(points):
    iters, nu = 1, 0.5
    dim = len(points[0])

    def deriv(a):
        return [
            sum(2 * (a[0] * p[0] + a[1] * p[1] + a[2] - p[2]) * p[0] for p in points),
            sum(2 * (a[0] * p[0] + a[1] * p[1] + a[2] - p[2]) * p[1] for p in points),
            sum(2 * (a[0] * p[0] + a[1] * p[1] + a[2] - p[2])        for p in points)
        ]

    linear = [0, 0, 0]
    for iter in range(iters):
        goto = deriv(linear)
        for i in range(dim):
            linear[i] -= nu * goto[i]

    return Linear(linear[0], linear[1], linear[2])
