
import os
import sys
sys.path.append('..')
sys.path.append('../..')
import argparse
import utils
import itertools
import random
from student_utils import *
import networkx as nx
from dijkstar import Graph, find_path

#def generateOutput():


def createEdge(numEdges, maxWeight, graph=Graph, u=int, setOfVAndWeight=list):
	#for v, w in setOfVAndWeight:
	#	graph.add_edge(u, v, w)
    return

def matrixConvert(graph, num):
    ret = ""
    for i in range(num):
        if (i in nx.nodes(graph)):
            for j in range(num):
                if (j in nx.neighbors(graph, i)):
                    ret += str(graph.edges[i,j]['weight']) + " "
                else:
                    ret += "x "
            ret = ret[:len(ret) - 1]
            ret += "\n"
        else:
            for i in range(num):
                ret += "x "
            ret = ret[:len(ret) - 1]
            ret += "\n"
    return ret


def randomGen(graph, n, numEdges, maxWeight):
    edges = []
    r = range(n)
    for i in r:
        for j in range(i, n):
            if i != j:
                edges.append((i,j))
    samp = random.sample(edges, numEdges)
    for k in samp:
        w = random.sample(range(1, maxWeight), 1)[0]
        graph.add_edge(k[0], k[1], weight = w)
        graph.add_edge(k[1], k[0], weight = w)
    return graph

if __name__ == "__main__":
	print("yuh bitch")

	first = ["Chelm", "Elm", "El", "Bur", "En", "Eg", "Pem", "Pen", "Edg", "Sud", "Sod", "Hors", "Dur", "Sun", "Nort", "Brad", "Farn", "Barn", "Dart", "Hart", "South", "Shaft", "Blan", "Rock", "Alf", "Wy", "Marl", "Staf", "Wet", "Cas", "Stain", "Whit", "Stap", "Brom", "Wych", "Watch", "Win", "Horn", "Mel", "Cook", "Hurst", "Ald", "Shriv", "Kings", "Clere", "Maiden", "Leather", "Brack","Brain", "Walt", "Prest", "Wen", "Flit", "Ash"]
	last = ["ford", "stoke", "ley", "ney",  "don", "den", "ton", "bury", "well", "beck", "ham", "borough", "side", "wick", "hampton", "wich", "cester", "chester", "ling", "moor", "wood", "brook", "port", "wold", "mere", "castle", "hall", "bridge", "combe", "smith", "field", "ditch", "wang", "over", "worth", "by", "brough", "low", "grove", "avon", "sted", "bourne", "borne", "thorne", "lake", "shot", "bage", "head", "ey", "nell", "tree", "down"]

def randomGenCheck(graph, i, j, k):
    g = randomGen(graph, i, j, k)
    its = 1
    while (not is_metric(g)):

        g = randomGen(nx.Graph(), i, j, k)
        its += 1
    print(matrixConvert(g, i))
    print(g.adj)
    print(its)
    return g

	# locations = ["Soda",  "Dwinelle", "Wheeler", "Campanile", "Cory", "RSF", "Barrows"]

	# edges = {
	# 	0: [ (1,1), (3,1), (6,1)],
	# 	1: [ (0,1), (3,1)],
	# 	2: [ (3,1), ],
	# 	3: [ (0,1), (1,1), (2,1), (4,1), (5,1), (6,1)],
	# 	4: [ (3,1) ],
	# 	5: [ (3,1) ],
	# 	6: [ (0,1), (3,1)]
	# }
graph = nx.Graph()
	# for u in edges.keys():
	# 	incidentEdges = edges[u]
	# 	#print(labeledEdges)
	# 	createEdge(graph, u, incidentEdges)
graph = randomGenCheck(graph, 20, 40, 5)
print(graph)
	# #print(find_path(graph, 0, 4))
