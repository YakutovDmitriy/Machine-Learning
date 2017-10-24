from misc import *
from fair_linear import fair_linear
from descent_linear import descent_linear
from genetic_linear import genetic_linear
from draw import *
import threading

def test_linear(data, linear):
    eprint("Start test")
    eprint.enter()
    # for p in data:
    #     eprint("%8s %8s : %8s %8s" % tuple(("%.2f %.2f %.2f %.2f" % (p[0], p[1], p[2], linear(p[0], p[1]))).split()))
    xs, ys, zs = zip(*data)
    draw(xs, ys, zs, linear)
    # while ask('Do you want to test some point?'):
    #     eprint("Enter area and number of rooms:", end=' ')
    #     area, rooms = map(float, input().strip().split())
    #     eprint("Expected price of such flat is %.2f" % linear(area, rooms))
    eprint.exit()

graphs = []
for setting_method in (fair_linear, descent_linear, genetic_linear):
    eprint("Start %s method:" % setting_method.__name__.split('_')[0])
    eprint.enter()
    data = read_csv("prices_all.csv")[1:]
    for x in data:
        for i in range(len(x)):
            x[i] = float(x[i])
    graph, linear = setting_method(data)
    graphs.append(graph)
    eprint("Linear function is %s with std %.4f" % (linear, linear.std(data)))
    # test_linear(data, linear)
    eprint.exit()

build_graph(graphs)
