
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

import random
import copy

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
    maxWeight = int(max_weight / 2)

    while (len(edgesToAdd) != 0):
        toVertex = random.sample(edgesToAdd, 1)[0]
        print(toVertex)

        edgesToAdd.remove(toVertex)

<<<<<<< HEAD
		graph.add_edge(vertexLastAdded, toVertex, weight=weight)
		vertexLastAdded = toVertex

	weight = random.randint(1, maxWeight)
	graph.add_edge(vertexLastAdded, 0, weight=weight)
=======
        weight = random.randint(1, maxWeight)

        graph.add_edge(vertexLastAdded, toVertex, weight=weight)
        #graph.add_edge(toVertex, vertexLastAdded, weight=weight)
        vertexLastAdded = toVertex
    
    weight = random.randint(1, maxWeight)
    graph.add_edge(vertexLastAdded, 0, weight=weight)
	#graph.add_edge(0, vertexLastAdded, weight=weight)
>>>>>>> b2619c1ebcc90a8c7b8718ff741103cf2a3787c8


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
    samp = random.sample(edges, numEdges + n)
    its = 0
    for k in samp:
        print(its)
        count = 0
        w = random.sample(range(1, maxWeight), 1)[0]
        graph.add_edge(k[0], k[1], weight = w)
        #graph.add_edge(k[1], k[0], weight = w)
        while (not is_metric(graph) and count < 10):
            graph.remove_edge(k[0], k[1])
            w = random.sample(range(1, maxWeight), 1)[0]
            graph.add_edge(k[0], k[1], weight = w)
            count = count + 1

        if (not is_metric(graph)):
            print("had remove")
            graph.remove_edge(k[0], k[1])

        its = its + 1
    #return graph

def randomGenCheck(graph, i, j, k):
	gOld = copy.deepcopy(graph)
	g = randomGen(graph, i, j, k)
	its = 1
	while (not is_metric(g)):
		temp = copy.deepcopy(gOld)
		g = randomGen(nx.Graph(), i, j, k)
		gOld = temp
		its += 1

	print("asdada", its)
	#print(matrixConvert(g, i))
	#print(g.adj)
	#print(its)
	return g

def saveGraphToFile(graph, maxLocations, locations, houses):
	inputFileName = 'input/' + str(maxLocations) + '.in'
	utils.write_to_file(inputFileName, str(len(locations)) + '\n')
	utils.write_to_file(inputFileName, str(len(houses)) + '\n', append=True)

	stringsOfLocations = " ".join(locations)
	stringOfHouses = " ".join(houses)
	utils.write_to_file(inputFileName, stringsOfLocations + '\n', True)
	utils.write_to_file(inputFileName, stringOfHouses + '\n', True)
	utils.write_to_file(inputFileName, locations[0] + '\n', True)

	graphToMatrix = matrixConvert(graph, len(locations))
	utils.write_to_file(inputFileName, graphToMatrix, True)

def FindPath(graph, maxedge):
	g = copy.deepcopy(graph)
	min = maxedge
	at = 0
	edges = g.adj[0]
	print("her \n")
	print(edges)
	for e in edges:
		if (edges[e]['weight'] < min):
			min = edges[e]['weight']
			at = e# -*- coding: utf-8 -*-
	return (min, at)



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

<<<<<<< HEAD
	graph = randomGenCheck(graph, len(locations), 2*len(locations), args.w)

	#print(matrixConvert(graph, len(locations)))
	#print(graph.adj)
	print(FindPath(graph, args.w))
=======
    for c in nx.minimum_cycle_basis(graph, weight='weight'):
        print(c)
>>>>>>> b2619c1ebcc90a8c7b8718ff741103cf2a3787c8

    #graph = randomGen(graph, len(locations), 2*len(locations), args.w)
    randomGen(graph, len(locations), 2*len(locations), args.w)

    #graph = graph.to_directed()

    print(matrixConvert(graph, len(locations)))
    #print(graph.adj)

    saveGraphToFile(graph, args.l, locations, houses)


		# --- solution ------ #

	# for neighbor in nx.all_neighbors(graph, 0):
	# 	print(neighbor)

	# minEdge = None
	# edgeDict = dict()
	# for edge in list(nx.edges(graph, nbunch=[0])):
	# 	#edgeDict[edge] = graph[edge[0]][edge[1]]['weight']
	# 	print(edge, graph[edge[0]][edge[1]]['weight'])

	# minEdge = min(edgeDict, key=edgeDict.get)
	# print(minEdge)

	# graph.remove_edge(minEdge[0], minEdge[1])
	#print(matrixConvert(graph, len(locations)))
    housesDict = {}

    for house in houses:
        housesDict[locations.index(house)] = ([], float('inf'))

    startingLocation = 0
    minCycle = None
    for c in nx.minimum_cycle_basis(graph, weight='weight'):
        if (startingLocation in c and is_valid_walk(graph, c)):
            print(len(c))
            minCycle = c
            #break

    indexForStart = minCycle.index(startingLocation)
    minCycle = minCycle[indexForStart:] + minCycle[:indexForStart]
    print(minCycle)


	#print('path: ', nx.dijkstra_path(graph, minEdge[0], minEdge[1], weight='weight'))
	#print('shrt length: ', nx.dijkstra_path_length(graph, 0, locations.index(houses[1]), weight='weight'))

    for vertex in minCycle:
        for house in housesDict.keys():
            currMinWeight = housesDict[house][1]
            pathWeight = nx.dijkstra_path_length(graph, vertex, house, weight='weight')
            if (pathWeight < currMinWeight):
                path = nx.dijkstra_path(graph, vertex, house, weight='weight')

                housesDict[house] = (path, pathWeight)

	#print(housesDict)

    locationDict = {}
    for location in minCycle:
        locationDict[location] = []

    dropoffLocations = set()
    for house in housesDict.keys():
        path = housesDict[house][0]
        dropoff = path[0]
        locationDict[dropoff].append(house)
        dropoffLocations.add(dropoff)

    print(locationDict)

	# --- output timeeeeee --- #

    cycle = ' '.join([locations[vertex] for vertex in minCycle]) + ' ' + locations[startingLocation]
    print(cycle)
    print(dropoffLocations)

    numDropoffs = len(dropoffLocations)

    dropoffPaths = []
    for dropoff in dropoffLocations:
        path = locations[dropoff] + ' ' + ' '.join([locations[vertex] for vertex in locationDict[dropoff]])
        dropoffPaths.append(path)

    print(dropoffPaths)

    outputFileName = 'output/' + str(args.l) + '.out'


    utils.write_to_file(outputFileName, cycle + '\n')
    utils.write_to_file(outputFileName, str(numDropoffs) + '\n', append=True)
    for p in dropoffPaths:
        utils.write_to_file(outputFileName, p + '\n', append=True)

    print(graph.edges)

<<<<<<< HEAD



=======
	
	
>>>>>>> b2619c1ebcc90a8c7b8718ff741103cf2a3787c8



#   graph = nx.Graph()
# 	# for u in edges.keys():
# 	# 	incidentEdges = edges[u]
# 	# 	#print(labeledEdges)
# 	# 	createEdge(graph, u, incidentEdges)
#   graph = randomGenCheck(graph, 20, 40, 5)
#   print(graph)
	# #print(find_path(graph, 0, 4))

	# print(graph)
	# #print(find_path(graph, 0, 4))
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
