import os
import sys
sys.path.append('..')
sys.path.append('../..')
import argparse
import utils

from student_utils import *
import networkx as nx

import queue
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

    currQ = queue.Queue()
    visited = dict()

    visited[start] = 0
    currQ.queue = queue.deque([start])
    while (len(visited.keys()) < k + 1):
        newQ = queue.Queue()
        while(not currQ.empty()):
            currVertex = currQ.get()
            # print('c', currVertex, graph[currVertex])
            # print('g', graph[currVertex][list(graph[currVertex])[0]]['weight'])
            # print(visited[currVertex])
            neighbors = [(node, graph[currVertex][node]['weight'] + visited[currVertex]) for node in list(graph[currVertex])]
            #print("n", neighbors)
            for n in neighbors:
                visited[n[0]] = min(n[1], visited.get(n[0], float('inf')))
                newQ.put(n[0])
        
        #print(visited)
        currQ = newQ

    return sorted(list(visited.items()), key= lambda v: v[1])[:k+1]

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
    graph, message = adjacency_matrix_to_graph(adjacency_matrix)
    print("total list edges: ", list(graph.edges), "\n\n")
    for i in range(0, 3):
        print("edge 3: ", end='')
        edge = list(graph.edges)[i]
        print(edge, graph.get_edge_data(edge[0], edge[1]))

    homeIndicesInGraph = [list_of_locations.index(home) for home in list_of_homes]
    startingIndex = list_of_locations.index(starting_car_location)

    for home in homeIndicesInGraph:
        print(f"adjacent edges to {home}:  {graph[home]}")

    print("\n----------\n")
    k = 2
    nodesToDelete = set()
    for home in homeIndicesInGraph:
        print(f"cluster size {k} for {home}:")
        shortestKClusters = kClosestClusters(graph, home, k)
        print(f"fullCluster: {shortestKClusters} \n")

        nodesInCluster = [node[0] for node in shortestKClusters]
        clusterNode = Cluster(home)
        
        for node in nodesInCluster:
            nodesToDelete.add(node)
            neighbors = [x for x in list(graph[node]) if x not in nodesInCluster]

            


        break

    
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


        
