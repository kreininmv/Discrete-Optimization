#!/usr/bin/python
# -*- coding: utf-8 -*-

import itertools

import networkx as nx
import numpy.random as rnd
import matplotlib.pyplot as plt
import random

def calc(edges, node_count, edge_count, order, max_colour):
    colours = [[0]*node_count for i in range(node_count)]
    colour_dict = {a: 0 for a in range(0, edge_count)}
    colour_count = 0

    for l in range(0, node_count):
        flag = -1
        i = order[l][0]
        #i = l
        for k in range (0, node_count):
            j = order[k][0]
            #j = k
            if (colours[i][j] == 0):
                colours[i][j] = 1
                flag = j
                if (colour_dict[j] == 0):
                    colour_count += 1
                    colour_dict[j] = 1
                    if (colour_count >= max_colour):
                        return max_colour+1, [0]
                break
        
        for j in range(0, node_count):
            if (edges[i][j] != 0):
                colours[j][flag] = -1
            if (colours[i][j] == 0):
                colours[i][j] = -1
    
    solution = [0] * node_count
    
    for i in range(0, node_count):
        
        for j in range(0, node_count):
            if (colours[i][j] == 1):
                solution[i] = j        
                break

    return colour_count, solution

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    first_line = lines[0].split()
    node_count = int(first_line[0])
    edge_count = int(first_line[1])

    edges = [ [0]*node_count for i in range(node_count) ]
    count_edges = [0] * node_count

    for i in range(1, edge_count + 1):
        line = lines[i]
        parts = line.split()
        edges[int(parts[0])][int(parts[1])] = 1
        edges[int(parts[1])][int(parts[0])] = 1
        count_edges[int(parts[1])] += 1
        count_edges[int(parts[0])] += 1
    
    order = []
    for i in range(node_count):
        order.append((i, count_edges[i]))
    
    order.sort(key=lambda tup: tup[1], reverse = True)
    # build a trivial solution
    # every node has its own color
    #colour_count_1 = 0
    #colour_count_1, solution_1 = calc(edges, node_count, edge_count, order)
 #
    #order.sort(key=lambda tup: tup[1])
    #colour_count_2 = 0
    #colour_count_2, solution_2 = calc(edges, node_count, edge_count, order)
    #
    #order.sort(key=lambda tup: tup[0])
    #colour_count_0 = 0
    #colour_count_0, solution_0 = calc(edges, node_count, edge_count, order)
    #
    #if (colour_count_0 < colour_count_1 and colour_count_0 < colour_count_2):
    #    colour_count = colour_count_0
    #    solution = solution_0
    #elif (colour_count_1 < colour_count_2):
    #    colour_count = colour_count_1
    #    solution = solution_1
    #else:
    #    colour_count = colour_count_2
    #    solution = solution_2
    
    #print(order)
    colour_count = node_count
    for i in range(100000):
        random.shuffle(order)
        colour_count_0 = 0
        colour_count_0, solution_0 = calc(edges, node_count, edge_count, order, colour_count)

        if (colour_count_0 < colour_count):
            colour_count = colour_count_0
            solution = solution_0
            #print('xuy')
    
    #print(order)
    
    

    # prepare the solution in the specified output format
    output_data = str(colour_count) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))

    return output_data


import sys

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)')

