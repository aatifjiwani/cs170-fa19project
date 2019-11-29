import os
import sys
sys.path.append('..')
sys.path.append('../..')
import argparse
import utils

from student_utils import *
import networkx as nx

from queue import PriorityQueue
"""
======================================================================
  Complete the following function.
======================================================================
"""

class Cluster:
    def __init__(self, homeIndex):
        self.home = homeIndex

    def __repr__(self):
        return f"Cluster for home {self.home}"

    def __str__(self):
        return f"Cluster for home {self.home}"

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
    #print(list_of_locations)
    #print(adjacency_matrix)

    print()
    origGraph, message = adjacency_matrix_to_graph(adjacency_matrix)
    graph = nx.MultiGraph(origGraph)
    print("total list edges: ", list(graph.edges), "\n\n")

    homeIndicesInGraph = [list_of_locations.index(home) for home in list_of_homes]
    startingIndex = list_of_locations.index(starting_car_location)

    for home in homeIndicesInGraph:
        print(f"adjacent edges to {home}:  {graph[home]}")

    print("\n----------\n")
    k = 1
    closestKNodesToHome = dict()
    for home in homeIndicesInGraph:
        print(f"cluster size {k} for {home}:")
        shortestKClusters = kClosestClusters(graph, home, k)
        print(f"fullCluster: {shortestKClusters} \n")
        closestKNodesToHome[home] = shortestKClusters


    nodesToDelete = set()
    nodesToClusters = dict()
    homeClusters = dict()

    for home in homeIndicesInGraph:
        # print(f"cluster size {k} for {home}:")
        # shortestKClusters = kClosestClusters(graph, home, k)
        # print(f"fullCluster: {shortestKClusters} \n")

        clusterNode = Cluster(home)
        homeClusters[home] = clusterNode
        cluster = [x[0] for x in closestKNodesToHome[home]]
        for node in cluster:
            nodesToDelete.add(node)

            if node in nodesToClusters:
                for dupCluster in nodesToClusters[node]:
                    graph.add_edge(clusterNode, dupCluster, \
                        weight = 0, nodesCondensed = (node, node))

            for nbor in origGraph[node]:
                if nbor not in cluster:
                    weightofEdge = origGraph.get_edge_data(node, nbor)['weight']
                    if nbor in nodesToClusters:
                        for nborCluster in nodesToClusters[nbor]:
                           graph.add_edge(clusterNode, nborCluster, \
                                weight = weightofEdge, nodesCondensed = (node, nbor)) 
                    else:
                        graph.add_edge(clusterNode, nbor, \
                            weight = weightofEdge, nodesCondensed = (node, nbor))

            nodesToClusters[node] = nodesToClusters.get(node, []) + [clusterNode]


    print(3)
    
    pass





    

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
    solve(list_locations, list_houses, starting_car_location, adjacency_matrix, params=params)
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


        
