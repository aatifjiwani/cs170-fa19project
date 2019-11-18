import os
import sys
sys.path.append('..')
sys.path.append('../..')
import argparse
import utils
import itertools

from dijkstar import Graph, find_path

#def generateOutput():

<<<<<<< HEAD
if if __name__ == "__main__":
    print("yuh bitch")
=======

def createEdge(graph=Graph, u=int, setOfVAndWeight=list):
	for v, w in setOfVAndWeight:
		graph.add_edge(u, v, w)

if __name__ == "__main__":
	print("yuh bitch")

	first = ["Chelm", "Elm", "El", "Bur", "En", "Eg", "Pem", "Pen", "Edg", "Sud", "Sod", "Hors", "Dur", "Sun", "Nort", "Brad", "Farn", "Barn", "Dart", "Hart", "South", "Shaft", "Blan", "Rock", "Alf", "Wy", "Marl", "Staf", "Wet", "Cas", "Stain", "Whit", "Stap", "Brom", "Wych", "Watch", "Win", "Horn", "Mel", "Cook", "Hurst", "Ald", "Shriv", "Kings", "Clere", "Maiden", "Leather", "Brack","Brain", "Walt", "Prest", "Wen", "Flit", "Ash"]
	last = ["ford", "stoke", "ley", "ney",  "don", "den", "ton", "bury", "well", "beck", "ham", "borough", "side", "wick", "hampton", "wich", "cester", "chester", "ling", "moor", "wood", "brook", "port", "wold", "mere", "castle", "hall", "bridge", "combe", "smith", "field", "ditch", "wang", "over", "worth", "by", "brough", "low", "grove", "avon", "sted", "bourne", "borne", "thorne", "lake", "shot", "bage", "head", "ey", "nell", "tree", "down"]

	

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
>>>>>>> 33b8930b215cd91dde8d1aecd66afb4bc4b7d8c7
