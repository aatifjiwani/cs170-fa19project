import os
import sys
sys.path.append('..')
sys.path.append('../..')
import argparse
import utils
import itertools

from dijkstar import Graph, find_path
import networkx as nx

import random

#def generateOutput():
first = ["Chelm", "Elm", "El", "Bur", "En", "Eg", "Pem", "Pen", "Edg", "Sud", "Sod", "Hors", "Dur", "Sun", "Nort", "Brad", "Farn", "Barn", "Dart", "Hart", "South", "Shaft", "Blan", "Rock", "Alf", "Wy", "Marl", "Staf", "Wet", "Cas", "Stain", "Whit", "Stap", "Brom", "Wych", "Watch", "Win", "Horn", "Mel", "Cook", "Hurst", "Ald", "Shriv", "Kings", "Clere", "Maiden", "Leather", "Brack","Brain", "Walt", "Prest", "Wen", "Flit", "Ash"]
last = ["ford", "stoke", "ley", "ney",  "don", "den", "ton", "bury", "well", "beck", "ham", "borough", "side", "wick", "hampton", "wich", "cester", "chester", "ling", "moor", "wood", "brook", "port", "wold", "mere", "castle", "hall", "bridge", "combe", "smith", "field", "ditch", "wang", "over", "worth", "by", "brough", "low", "grove", "avon", "sted", "bourne", "borne", "thorne", "lake", "shot", "bage", "head", "ey", "nell", "tree", "down"]

def createLocationsAndHouses(maxLocations, maxHouses):
	names = itertools.product(first, last)
	names = [first + last for first,last in names]

	numLocations = int( (args.l / 2) + random.random() * (args.l / 2))
	numHouses = int( (args.t / 2) + random.random() * (args.t / 2) )

	locations = random.sample(names, numLocations)
	houses = random.sample(locations[1:], numHouses)

	return locations, houses

def createHamiltonianCycle(graph, max_weight=int, num_locations=int):
	edgesToAdd = [x for x in range(1, num_locations)]
	vertexLastAdded = 0
	maxWeight = max_weight

	while (len(edgesToAdd) != 0):
		toVertex = random.sample(edgesToAdd, 1)[0]
		edgesToAdd.remove(toVertex)

		weight = random.randint(1, maxWeight)

		graph.add_edge(vertexLastAdded, toVertex, weight=weight)
		vertexLastAdded = toVertex

	weight = random.randint(1, maxWeight)
	graph.add_edge(vertexLastAdded, 0, weight=weight)


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Parsing arguments')
	parser.add_argument('-l', type=int, help="Most locations")
	parser.add_argument('-t', type=int, help="Most homes")
	parser.add_argument('-w', type=int, help="Max weight")
	args = parser.parse_args()

	locations, houses = createLocationsAndHouses(args.l, args.t)

	print("locations: ", len(locations), " ", locations)
	print("houses: ", len(houses) , " ", houses)

	graph = nx.Graph()
	createHamiltonianCycle(graph, args.w, len(locations))
	
	print(graph.adj)



		
	




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
	# graph = Graph()
	# for u in edges.keys():
	# 	incidentEdges = edges[u]
	# 	#print(labeledEdges)
	# 	createEdge(graph, u, incidentEdges)

	# print(graph)
	# #print(find_path(graph, 0, 4))