#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
from collections import namedtuple

Point = namedtuple("Point", ['x', 'y'])


class node(object):

    # bound_length - минимальная длина в графе
    # matrix - матрица переходов
    # маршрут - массив, в котором описан порядок вершин
    # node_count - кол-во вершин
    def __init__(self, matrix, solution, bound_length, node_count):
        self.bound_length = bound_length
        self.matrix = matrix
        self.solution = solution
        self.node_count = node_count

def length(point1, point2):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

#функция удаления нужной строки и столбцах
def Delete(matr,index1,index2):
    matrix = [row[:] for row in matr] 
    
    del matrix[index1]
    for i in matrix:
        del i[index2]

    return matrix

# Считает длину решения
def calculate_length_of_tour(points, tour, node_count):
    
    sum_len = length(points[tour[0]], points[tour[node_count - 1]])

    for index in range(0, node_count-1):
        sum_len += length(points[tour[index]], points[tour[index+1]])

    return sum_len


def reduce_matrix(matrix, node_count):
    min_x = [0.0] * (node_count+1)
    
    for i in range(1, node_count+1):
        min_i = -1
        for j in range(1, node_count+1):
            if (i != j and matrix[i][j] < min_i):
                min_i = matrix[i][j]
            elif (i != j and min_i == -1):
                min_i = matrix[i][j]
        min_x[i] = min_i

    for i in range(1, node_count+1):
        for j in range(1, node_count+1):
            matrix[i][j] = matrix[i][j] - min_x[i]
    
    min_y = [0.0] * (node_count+1)
    for i in range(1, node_count+1):
        min_i = -1
        for j in range(1, node_count+1):
            if (i != j and matrix[j][i] < min_i):
                min_i = matrix[j][i]
            elif (i != j and min_i == -1):
                min_i = matrix[j][i]
        min_y[i] = min_i
    
    for i in range(1, node_count+1):
        for j in range(1, node_count+1):
            matrix[i][j] = matrix[i][j] - min_y[i]

    sum = 0
    for i in range(1, node_count+1):
        sum = sum + min_x[i] + min_y[i]

    return matrix, min_x, min_y, sum

def solver(matrix, node_count):
    matrix, min_x, min_y, sum = reduce_matrix(matrix, node_count)
    
    #В matrix теперь приведенная матрица, 

    #Заглушка для первоначального решения
    solution = [0] * node_count
    for i in range(0, node_count):
        solution[i] = i

    return solution

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')
    node_count = int(lines[0])

    #Здесь задаю изначальный массив точек, после подсчёта расстояний он уже не нужен
    points = []
    for i in range(1, node_count+1):
        line = lines[i]
        parts = line.split()
        points.append(Point(float(parts[0]), float(parts[1])))

    # build a trivial solution
    # visit the nodes in the order they appear in the file
    
    
    # Создаю матрицу переходов между вершинами, в каждой вершине написан стоимость перехода из одной в другую
    road_matrix = [[0.0]*(node_count+1) for i in range(node_count + 1)]
    
    # Заполняю нулевой столбец и строчку индексами вершин
    for i in range (0, node_count):
        road_matrix[0][i] = i
        road_matrix[0][i] = i

    # Заполняю матрицу расстояний
    for i in range(1, node_count + 1):
        for j in range(i, node_count + 1):
            if (i != j):
                road_matrix[i][j] = length(points[i-1], points[j-1])
                road_matrix[j][i] = road_matrix[i][j]
            else:
                road_matrix[i][j] = float('inf')
    
    # Вызываем саму функцию решения
    solution = solver(road_matrix, node_count)
    
    # Приводим решение в нормальный вид
    for i in range(0, node_count):
        solution[i] -= 1
    
    # Считаем длину пути
    obj = calculate_length_of_tour(points, solution, node_count)
    
    # prepare the solution in the specified output format
    output_data = '%.2f' % obj + ' ' + str(0) + '\n'
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
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/tsp_51_1)')

