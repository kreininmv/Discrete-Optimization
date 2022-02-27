class node(object):
    #   self   - сама вершина
    #   taken  - массив взятых вершин
    #   profit - 
    #   weight - вес
    #   level  - номер вершины
    def __init__(self, taken, profit, weight, level):
        self.taken = taken
        self.profit = profit
        self.weight = weight
        self.level = level

def solver(array, cap):
    # Аргументы функции:
    # l   - массив: стоимости, вес и индекса каждого элемента
    # cap - размер рюкзака 

    # Создаемм пустой корень вершины дерева перебора
    root = node([0 for i in range(len(array))], 0, 0, 0)

    # верхнее значение
    ub = calculate(root, cap, array)

    #нижнее значение
    lower_price = 0
    # лучшее значение
    best_price = 0
    # массив лучших элементов
    best_items = []

    # создаем очередь и добавляюм туда корень
    Q = [root]

    # пока очередь не пуста выполняем
    while Q:
        cur = Q.pop(0)

        # Создаем две ветки от текущей вершины, (в одной берем элемент, а вдругой нет)
        children = create_children(cur, array, cap)

        #Если есть еще элементы
        if (children != None): 
            for child in reversed(children): # переворачиваем, т.к. хотим сначала 
                boc = calculate(child, cap, array)   # Считаем прибыль у веток от этой вершины
                
                #Если прибыль меньше возможной лучшей и больше текущей лучшей, а вес набора не превышает размер рюкзака, то добавляем в очередь
                if (boc <= ub and boc >= best_price and child.weight <= cap):
                    # добавляем ребенка в очередь
                    Q = [child] + Q
        else:
            #Если уже не осталось элементов 
            #Ставим нижнюю границу
            lower_price = calculate(cur, cap, array)
            
            if (lower_price > best_price): # обновляем лучший элемент
                best_price = lower_price
                best_items = cur.taken # обновляем список элементов, которые будем брать
    
    return best_price, best_items


#Функция для создания детей у вершины
def create_children(n, array, cap):
    
    if (len(array[n.level:]) == 0): 	# Если это последний элемент в массиве
        return None

    first = array[n.level:][0]  	# берем первый элемент после этой вершины
    taken = n.taken[:]      		# копируем массив взятых элементов
    taken[array.index(first)] = 1       # обновляем первую позицию из взятого списка

    # Создаем первую вершину с взятым элементом
    child1 = node(taken, n.profit + first[0], n.weight + first[1], n.level + 1)

    # Создаем вторую вершину без взятого первого элемента
    child2 = node(n.taken, n.profit, n.weight, n.level + 1)

    # Возвращаем список детей
    return [child1, child2]

price_dict = {} #Словарь прибыли от вершины

def calculate(node, cap, array):
    n = len(array)
    total_weight = 0
    
    if (node.weight > cap):             # если текущий вес элемента больше размера рюкзака
        return 0
    elif ((node, cap) in price_dict):  	# ищем в словаре есть ли уже- такая вершина, и возвращаем её прибыль
        return price_dict[(node, cap)]
    else:
        max_price = node.profit     	# прибыль
        total_weight = node.weight  	# текущий вес равен вершине
        j = node.level              	# j - номер вершины в массиве, чтобы пробежать оставшиеся

        # продолжаем цикл, пока не закончатся элементы или следующий элемент не вместится в рюкзак
        while (j < n and (total_weight + array[j][1] <= cap)): 
            total_weight = total_weight + array[j][1]
            max_price += array[j][0]    
            j += 1
                  
        # Если осталось места, то считаем недополученную прибыль: свободное место в рюкзаке * удельную стоимсть следующего элемента
        if (j < n):   
            max_price = max_price + int((cap - total_weight) * (float(array[j][0])  / array[j][1]))
        
        price_dict[(node, cap)] = max_price #добавляем максимальную прибыль этой вершины

        return max_price

def solve_it(inputData):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = inputData.split('\n')

    firstLine = lines[0].split()
    no_of_items = int(firstLine[0])
    capacity = int(firstLine[1])

    #Массив: цены, веса и индекса
    items_list = []

    for i in range(1, no_of_items+1):
        line = lines[i]
        parts = line.split()
        items_list.append((int(parts[0]), int(parts[1]), i-1))

    #Сортируем по удельной стоимости
    items_list.sort(key=lambda tup: float(tup[0])/tup[1], reverse = True)

    #Запускаем solver, оптравляя массив и размер рюкзака
    value, item_taken = solver(items_list, capacity)

    #Заполняем массив взятых вещей
    taken = [0 for i in range(no_of_items)]
    for i in range(len(item_taken)):
        if item_taken[i] == 1:
            taken[items_list[i][2]] = 1

    outputData = str(value) + ' ' + str(1) + '\n'
    outputData += ' '.join(map(str, taken))
    return outputData


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')

