import os
import sys
sys.path.append('..')
sys.path.append('../..')
import argparse
import utils
import mlrose
import numpy as np
import traceback

from student_utils import *
import networkx as nx

from queue import PriorityQueue
"""
======================================================================
  Complete the following function.
======================================================================
"""

class Cluster:
    def __init__(self, homes = list, nodes = list):
        self.home = homes
        self.nodes = nodes

    def __repr__(self):
        return "Cluster for home " + ' and '.join(str(x) for x in self.home)

    def __str__(self):
        return "Cluster for home " + ' and '.join(str(x) for x in self.home)

    def home(self):
        return self.home

def kClosestClusters(graph, start, k):
    elementsInCluster = [] # (node, weight)
    pq = PriorityQueue()
    pq.put((0, start)) # (weight, node)
    while (len(elementsInCluster) < k + 1 and not pq.empty()):
        weight, poppedNode = pq.get()
        if poppedNode not in elementsInCluster:
            elementsInCluster.append((poppedNode, weight))
            for nbor in graph[poppedNode]:
                pq.put(( weight + graph[poppedNode][nbor][0]['weight'], nbor ))
    
    return elementsInCluster

def findKClusters(graph, homeIndicesInGraph, k):
    closestKNodes = [] # (set(), [])
    #closestKNodesToHome = dict()
    for home in homeIndicesInGraph:
        #print(f"cluster size {k} for {home}:")
        shortestKClusters = set([x[0] for x in kClosestClusters(graph, home, k)])
        #print(f"fullCluster: {shortestKClusters} \n")
        #closestKNodesToHome[home] = shortestKClusters
        found = False
        clusterList = []
        for cluster in closestKNodes:
            nodesInCluster, _ = cluster
            if not nodesInCluster.isdisjoint(shortestKClusters):
                clusterList.append(cluster)
                found = True
        
        if not found:
            closestKNodes.append((shortestKClusters, [home]))
        else:
            merged = set()
            totalHomes = set()
            for cluster in clusterList:
                nodesInCluster, forHomes = cluster
                closestKNodes.remove(cluster)
                merged = merged.union(nodesInCluster)
                totalHomes = totalHomes.union(forHomes)

            merged = merged.union(shortestKClusters)
            totalHomes = list(totalHomes.union(set([home])))

            closestKNodes.append((merged, totalHomes))


    return closestKNodes

def addClustersToGraph(graph, origGraph, closestKNodes):
    nodesToDelete = set()
    nodesToClusters = dict()
    homeClusters = dict()

    for cluster in closestKNodes:
        nodesInCluster, taHomes = cluster
        nodesInCluster = list(nodesInCluster)
        clusterNode = Cluster(homes=taHomes, nodes=nodesInCluster)

        for home in taHomes:
            homeClusters[home] = clusterNode

        for node in nodesInCluster:
            nodesToDelete.add(node)

            for nbor in origGraph[node]:
                if nbor not in nodesInCluster:
                    weightofEdge = origGraph.get_edge_data(node, nbor)['weight']
                    if nbor in nodesToClusters:
                        nborCluster = nodesToClusters[nbor]
                        graph.add_edge(clusterNode, nborCluster, \
                            weight=weightofEdge, condensed=(node, nbor))
                    else:
                        graph.add_edge(clusterNode, nbor, \
                            weight = weightofEdge, condensed=(node, nbor))

            nodesToClusters[node] = clusterNode

    return nodesToDelete, nodesToClusters, homeClusters

def findTSPPath(graph, nodesToClusters, homeClusters, startingIndex ):
    homes = set()

    if (startingIndex in nodesToClusters):
        homes.add(nodesToClusters[startingIndex])
    else:
        homes.add(startingIndex)
    
    for i in homeClusters.values():
        homes.add(i)

    homes = list(homes)

    dist_list = []
    #print(homes)
    g = graph

    shortest_paths = dict(nx.all_pairs_dijkstra(g, weight = 'weight'))
    for i in shortest_paths.keys():
        for j in shortest_paths[i][0].keys():
            if (not i == j) and (i in homes) and (j in homes):
                #print((i,j, shortest_paths[i][0][j]))
                #print("\n")

                blah = shortest_paths[i][0][j]
                if blah == 0:
                    blah = 0.01


                dist_list.append((homes.index(i), homes.index(j), blah ))

    fitness_dists = mlrose.TravellingSales(distances = dist_list)
    problem_fit = mlrose.TSPOpt(length = len(homes), fitness_fn = fitness_dists, maximize=False)
    best_state, best_fitness = mlrose.genetic_alg(problem_fit)

    return homes, shortest_paths, best_state

def findDTHPath(graph, fullClusterPath, startingIndex, nodesToClusters, shortest_paths_original, homeIndices):
    currentIndex = startingIndex
    fullPath = []
    dropOffLocations = dict()
    totalWeight = 0

    #indicies
    for nodeInPath in fullClusterPath[1:]:
        runningMinWeight = float('inf')
        runningMinPath = None
        nodeToGoTo = None
        if nodeInPath == fullClusterPath[-1]:
            runningMinWeight = shortest_paths_original[currentIndex][0][startingIndex]
            runningMinPath = shortest_paths_original[currentIndex][1][startingIndex]
            nodeToGoTo = startingIndex
        elif (type(nodeInPath) == Cluster):
            nodesCluster = nodeInPath.nodes
            for n in nodesCluster:
                weight = shortest_paths_original[currentIndex][0][n]
                if (weight < runningMinWeight):
                    nodeToGoTo = n
                    runningMinWeight = weight
                    runningMinPath = shortest_paths_original[currentIndex][1][n]
        elif (type(nodeInPath) == int):
            nodeToGoTo = nodeInPath
            runningMinWeight = shortest_paths_original[currentIndex][0][nodeInPath]
            runningMinPath = shortest_paths_original[currentIndex][1][nodeInPath]
        else:
            raise Exception

        totalWeight += (2/3)*runningMinWeight

        for vertex in runningMinPath:
            if vertex in nodesToClusters:
                cluster = nodesToClusters[vertex]
                for tahome in cluster.home:
                    weight = shortest_paths_original[vertex][0][tahome]
                    currDropoff, currMin = dropOffLocations.get(tahome, (None, float('inf')))
                    if (weight < currMin):
                        dropOffLocations[tahome] = (vertex, weight)

                        if (currMin == float('inf')):
                            totalWeight = totalWeight + weight
                        else:
                            totalWeight = totalWeight - currMin
                            totalWeight = totalWeight + weight

        fullPath += runningMinPath[:-1]
        currentIndex = nodeToGoTo

    fullPath += [startingIndex]

    for home in homeIndices:
        if home not in dropOffLocations:
            print('this home did not get dropped off', home)
            totalWeight = float('inf')
            break


    return fullPath, dropOffLocations, totalWeight

def generateDefaultSolution(startingIndex, homeIndices):
    bestDropoffLocations = dict()
    for taHome in homeIndicesInGraph:
        bestDropoffLocations[taHome] = (startingIndex, -1)

    bestFullPath = [ startingIndex, startingIndex ]

    return bestFullPath, bestDropoffLocations

def solve(list_of_locations, list_of_homes, starting_car_location, adjacency_matrix, params=[]):
    """
    Write your algorithm here.
    Input:
        list_of_locations: A list of locations such that node i of the graph corresponds to name at index i of the list
        list_of_homes: A list of homes
        starting_car_location: The name of the starting location for the car
        adjacency_matrix: The adjacency matrix from the input file
    Output:
        A list of locations representing the car path
        A list of (location, [homes]) representing drop-offs
    """

    origGraph, message = adjacency_matrix_to_graph(adjacency_matrix)
    shortest_paths_original = dict(nx.all_pairs_dijkstra(origGraph, weight = 'weight'))

    homeIndicesInGraph = [list_of_locations.index(home) for home in list_of_homes]
    startingIndex = list_of_locations.index(starting_car_location)
    nodesToClusters = dict()
    try:
        k = -1
        bestDropoffLocations = None
        bestFullPath = None
        bestTotalWeight = float('inf')
        countInfinity = 0
        while(len(nodesToClusters.keys()) != len(list_of_locations) \
            and countInfinity < 3 and k < 100):
            k = k+1
            graph = nx.MultiGraph(origGraph)
            closestKNodes = findKClusters(graph, homeIndicesInGraph, k)

            nodesToDelete, nodesToClusters, homeClusters = addClustersToGraph(graph, origGraph, closestKNodes)

            for node in nodesToDelete:
                graph.remove_node(node)

            homes, shortest_paths, best_state = findTSPPath(graph, nodesToClusters, homeClusters, startingIndex)
            
            best_state = list(best_state)

            if startingIndex in nodesToClusters:
                isBest = best_state.index(homes.index(nodesToClusters[startingIndex]))
            else:
                isBest = best_state.index(homes.index(startingIndex))

            best_state = best_state[isBest:] + best_state[:isBest]

            path = [homes[index] for index in list(best_state)]
            path = path[1:] + path[:1]
            
            fullClusterPath = [path[-1]]
            for i in range(-1, len(path) - 1):
                full = shortest_paths[path[i]][1][path[i+1]][1:-1]
                fullClusterPath = fullClusterPath + full + [path[i + 1]]

            fullPath, dropOffLocations, totalWeight = findDTHPath(graph, fullClusterPath, startingIndex, \
                nodesToClusters, shortest_paths_original, homeIndicesInGraph)

            print("For k = ", k, "----")
            print("full path: ", fullPath)
            #print("dropOffLocations: ", dropOffLocations)
            print("total weight: ", totalWeight, "\n")

            if (totalWeight < bestTotalWeight):
                bestTotalWeight = totalWeight
                bestDropoffLocations = dropOffLocations
                bestFullPath = fullPath
            elif(totalWeight == float('inf')):
                countInfinity = countInfinity + 1

    except Exception:
        #traceback.print_exc()
        print("\n max k limit reached")
        pass

    if (bestTotalWeight == float('inf')):
        bestFullPath, bestDropoffLocations = generateDefaultSolution(startingIndex, homeIndicesInGraph)

    dropoffPointsToHomes = dict()
    for taHome in bestDropoffLocations.keys():
        dropOffPoint, _ = bestDropoffLocations[taHome]
        dropoffPointsToHomes[dropOffPoint] = dropoffPointsToHomes.get(dropOffPoint, []) + [taHome]
        
    return bestFullPath, dropoffPointsToHomes

def startSolver(list_locations, list_houses, starting_car_location, adjacency_matrix, \
    input_file, output_directory):

    fullPath, dropOffLocations = solve(list_locations, list_houses, starting_car_location, adjacency_matrix)

    basename, filename = os.path.split(input_file)
    output_filename = utils.input_to_output(filename)
    output_file = output_directory + '/' + output_filename
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    pathString = ''
    dropOffStrings = []
    lenDropOffs = len(dropOffLocations.keys())
    for node in fullPath:
        pathString += list_locations[node] + ' '
        if (node in dropOffLocations):
            string = str(list_locations[node]) + ' '
            for h in dropOffLocations[node]:
                string += str(list_locations[h]) + ' '
            string = string.strip()
            dropOffStrings.append(string)
            dropOffLocations.pop(node, None)

    pathString = pathString.strip()
    pathString += '\n'
    pathString += str(lenDropOffs) + '\n'
    pathString += '\n'.join(dropOffStrings)

    utils.write_to_file(output_file, pathString)






"""
======================================================================
   No need to change any code below this line
======================================================================
"""

"""
Convert solution with path and dropoff_mapping in terms of indices
and write solution output in terms of names to path_to_file + file_number + '.out'
"""
def convertToFile(path, dropoff_mapping, path_to_file, list_locs):
    string = ''
    for node in path:
        string += list_locs[node] + ' '
    string = string.strip()
    string += '\n'

    dropoffNumber = len(dropoff_mapping.keys())
    string += str(dropoffNumber) + '\n'
    for dropoff in dropoff_mapping.keys():
        strDrop = list_locs[dropoff] + ' '
        for node in dropoff_mapping[dropoff]:
            strDrop += list_locs[node] + ' '
        strDrop = strDrop.strip()
        strDrop += '\n'
        string += strDrop
    utils.write_to_file(path_to_file, string)

def solve_from_file(input_file, output_directory, params=[]):
    print('Processing', input_file)

    input_data = utils.read_file(input_file)
    num_of_locations, num_houses, list_locations, list_houses, starting_car_location, adjacency_matrix = data_parser(input_data)
    
    
    startSolver(list_locations, list_houses, starting_car_location, adjacency_matrix, \
        input_file, output_directory)
    # car_path, drop_offs = solve(list_locations, list_houses, starting_car_location, adjacency_matrix, params=params)

    # basename, filename = os.path.split(input_file)
    # output_filename = utils.input_to_output(filename)
    # output_file = f'{output_directory}/{output_filename}'
    # if not os.path.exists(output_directory):
    #     os.makedirs(output_directory)
    
    # convertToFile(car_path, drop_offs, output_file, list_locations)


def solve_all(input_directory, output_directory, params=[]):
    input_files = utils.get_files_with_extension(input_directory, 'in')

    for input_file in input_files:
        solve_from_file(input_file, output_directory, params=params)


if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Parsing arguments')
    parser.add_argument('--all', action='store_true', help='If specified, the solver is run on all files in the input directory. Else, it is run on just the given input file')
    parser.add_argument('input', type=str, help='The path to the input file or directory')
    parser.add_argument('output_directory', type=str, nargs='?', default='.', help='The path to the directory where the output should be written')
    parser.add_argument('params', nargs=argparse.REMAINDER, help='Extra arguments passed in')
    args = parser.parse_args()
    output_directory = args.output_directory
    if args.all:
        input_directory = args.input
        solve_all(input_directory, output_directory, params=args.params)
    else:
        input_file = args.input
        solve_from_file(input_file, output_directory, params=args.params)
