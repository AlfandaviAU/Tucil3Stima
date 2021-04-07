import networkx as nx
import matplotlib.pyplot as plt
from math import radians, cos, sin, asin, sqrt

place = []
koordinat = []
heu = []

#Array to Dictionary
def conv(x):
    graph = {}
    for row in range(len(x)):
        val = {}
        for col in range(len(x)):
            if (float(x[row][col]) != 0):
                val_key = col
                val_value = float(x[row][col])
                val[val_key] = val_value
        key = row
        graph[key] = val
    
    return graph

def read_coor(file):
    with open(file) as f:
        content = f.readlines()
    for i in content:
        x = i.replace('\n','')
        y = x.split('   ')
        z = y[1].split(', ')
        place.append(y[0])
        koordinat.append(z)
    
    for i in koordinat:
        for j in range(len(i)):
            temp = float(i[j])
            i[j] = temp

def read_bool_matrix(file):
    with open(file) as f:
        content = f.readlines()
    res = []
    for i in content:
        x = i.replace('\n','')
        y = x.split(' ')
        res.append(y)
    weightedpathgen(res)
    print(res)
    return res

def weightedpathgen(arr):
    print("awal",arr)
    for i in range(len(arr)):
        for j in range(len(arr[i])):
            if (arr[i][j] == '1'):
                arr[i][j] = harvesine(koordinat[i],koordinat[j])
            else :
                arr[i][j] = 0

def show():
    print("Kode        place                          Koordinat")
    for i in range(len(place)):
        num1 = len("Kode        ")
        num2 = len("place                          ")
        print(i," "*(num1 - len(str(i)) - 1),end="")
        print(place[i]," "*(num2 - (len(place[i])) - 1),end="")
        print(koordinat[i][0]," , ",koordinat[i][1])

def harvesine(point1, point2):
    lat1 = point1[0]
    lat2 = point2[0]
    lon1 = point1[1]
    lon2 = point2[1]  
    lon1 = radians(lon1)
    lon2 = radians(lon2)
    lat1 = radians(lat1)
    lat2 = radians(lat2)
    dlon = lon2 - lon1 
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * asin(sqrt(a)) 
    return(c * 6371000)

def heuristicgen(dest):
    for i in koordinat:
        heu.append(harvesine(koordinat[dest],i))
    print(heu)

def read_file (files):
    with open(files) as f:
        content = f.readlines()
    res = []
    for i in content:
        x = i.replace('\n','')
        y = x.split(' ')
        res.append(y)
    return res

cost = []
active = []
possibilities = []
p = []


def minimum(array) :
    mins = 1000000
    idx = 0
    for i in range(len(array)):
        if (array[i] < mins):
            mins = array[i]
            idx = i 

    return idx


def searchActivePath(x,arr):
    if (len(arr) == 1):
        return list(arr)
    else :
        for i in range(len(arr)):
            if (arr[i][len(arr[i]) - 1] == x):
                temp = list(arr[i])
        print(temp)
        return temp


def getActive_Cost(a,graph):
    temp = dict(graph[a])
    for i in (graph[a].keys()):
        active.append(i)
        x = temp[i] + heu[i]
        cost.append(x)
    print("Active & Cost:",active,cost)

def getListKey(a, graph):
    return list(graph[a].keys())

def Pathgen(list_key,arr):
    temp = []
    for i in range(len(list_key)):
        temp.append(list(arr))
        temp[i].append(list_key[i])
    print("Possible Path",temp)
    return temp

def remove(x):
    if (len(p) == 1):
        p.pop(0)
    else :
        for i in range(len(p)):
            if (p[i] == x):
                p.pop(i)

def generate(x):
    getActive_Cost(x,bobot)
    key = getListKey(x,bobot)
    path = searchActivePath(x,p)
    temp = Pathgen(key,path)
    remove(path)
    for i in temp:
        p.append(i)
    print(p)

def constructing():
    idx = minimum(cost)
    new_active = active[idx]
    active.pop(idx)
    cost.pop(idx)
    return new_active

def FindCost(arr):
    sum = 0
    for i in range(len(arr)-1):
        temp = bobot[arr[i]]
        price = temp[arr[i+1]]
        sum+= price
    print("Travel Cost =",sum) 

def search(start,end):
    i = 0
    heuristicgen(end)
    p.append(start)
    while(True):
        generate(start)
        start = constructing()
        if (start == end):
            fin = searchActivePath(end,p)
            print("Path Found =",fin)
            FindCost(fin)
            break

# Visualisasi
def drawFromTxt(arr):
    nodes = []
    weighted_edge = []
    for i in range(len(arr)):
        nodes.append(i)
        for j in range(len(arr[i])):
            if i != j:
                weighted_edge.append((i, j, int(arr[i][j])))

    graph = nx.Graph()
    graph.add_nodes_from(nodes)
    graph.add_weighted_edges_from(weighted_edge)

    options = {
        'nodes_color': 'blue',
        'nodes_size': 300,
        'width': 1,
    }
    nx.draw(graph, with_labels=True, font_weight='normal', **options)
    plt.show()

#Array yang dimiliki
#cost : biaya untuk melakukan perjalanan
#active : nodes active untuk diexpand adjacentnya
#bobot : bobot untuk perjalanan dari nodes 1 ke nodes lain g(n)
#heu : bobot heuristic terhadap suatu destinasi
#p = kemungkinan path yang sudah dibangkitkan

#Setup data
read_coor("coor1.txt")
x1 = read_bool_matrix("mat1.txt")
bobot = conv(x1)
show()
print(bobot)
start = int(input("Start : "))
finish = int(input("Finish : "))
search(start,finish)

# G = nx.Graph()
# nodes = ["Arad", "Bucharest", "Craiova", "Dobreta", 
#         "Eforie", "Fagaras", "Giurgiu", "Hirsova", "Lasi",
#         "Lugoj", "Mehadia", "Neamt", "Oradea", "Pitesti",
#         "Rimnicu Vilea", "Sibiu", "Timisoara", "Urziceni",
#         "Vaslusi", "Zerind"]


# weighted_edges = [
#     ("Arad", "Zerind", 75), ("Zerind", "Oradea", 71), ("Arad", "Timisoara", 118),
#     ("Vaslusi", "Lasi", 92), ("Lasi", "Neamt", 87),
#     ("Oradea", "Sibiu", 151), ("Arad", "Sibiu", 140), ("Timisoara", "Lugoj", 111),
#     ("Lugoj", "Mehadia", 70), ("Mehadia", "Dobreta", 75), ("Dobreta", "Craiova", 120),
#     ("Craiova", "Rimnicu Vilea", 146), ("Craiova", "Pitesti", 138), ("Pitesti", "Rimnicu Vilea", 97),
#     ("Sibiu", "Rimnicu Vilea", 80), ("Sibiu", "Fagaras", 99), ("Fagaras", "Bucharest", 211),
#     ("Pitesti", "Bucharest", 101), ("Bucharest", "Giurgiu", 90), ("Bucharest", "Urziceni", 85),
#     ("Urziceni", "Hirsova", 98), ("Hirsova", "Eforie", 85), ("Urziceni", "Vaslusi", 142)
# ]

# G.add_nodes_from(nodes)
# G.add_weighted_edges_from(weighted_edges)

# options = {
#     'nodes_color': 'blue',
#     'nodes_size': 300,
#     'width': 1,
# }

# print(list(G.nodes))
# print(list(G.edges))
# for n, nbrs in G.adj.items():
#    for nbr, eattr in nbrs.items():
#        wt = eattr['weight']
#        if wt > 0: print(f"({n}, {nbr}, {wt})")

# nx.draw(G, with_labels=True, font_weight='normal', **options)
# plt.show()

