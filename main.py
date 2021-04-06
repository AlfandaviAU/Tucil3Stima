import networkx as nx
import matplotlib.pyplot as plt



#Membaca file kemudian memasukkanya ke Array
def bacaFile (files):
    with open(files) as f:
        content = f.readlines()
    nice = []
    for i in content:
        x = i.replace('\n','')
        y = x.split(' ')
        nice.append(y)
    return nice

x = bacaFile("tes1.txt")

#Mengubah Array menjadi Dictionary
def convert(x):
    graf = {}
    for row in range(len(x)):
        val = {}
        for col in range(len(x)):
            if (int(x[row][col]) != 0):
                val_key = col
                val_value = int(x[row][col])
                val[val_key] = val_value
        key = row
        graf[key] = val
    
    return graf

cost = []
active = []
possibilities = []
p = []
z = convert(x)

def minArray(array) :
    temp = array[0]
    indeks = 0
    for i in range(len(array)):
        if (array[i] < temp):
            temp = array[i]
            indeks = i 

    return indeks


def pathfinder(x,arr):
    if (len(arr) == 1):
        return list(arr)
    else :
        for i in range(len(arr)):
            if (arr[i][len(arr[i]) - 1] == x):
                temp = list(arr[i])
        print(temp)
        return temp


def getActive_Cost(a,graf):
    temp = dict(graf[a])
    for i in (graf[a].keys()):
        active.append(i)
        cost.append(temp[i])
    print("aktif dan cost",active,cost)

def getKey(a,graf):
    return list(graf[a].keys())

def initPath(list_key,arr):
    temp = []
    for i in range(len(list_key)):
        temp.append(list(arr))
        temp[i].append(list_key[i])
    print("Possible Path",temp)
    return temp



def delX(x):
    if (len(p) == 1):
        p.pop(0)
    else :
        for i in range(len(p)):
            if (p[i] == x):
                p.pop(i)


def generate(x):
    getActive_Cost(x,z)
    key = getKey(x,z)
    path = pathfinder(x,p)
    temp = initPath(key,path)
    delX(path)
    for i in temp:
        p.append(i)
    print(p)

def constructing():
    indeks = minArray(cost)
    new_active = active[indeks]
    active.pop(indeks)
    cost.pop(indeks)
    return new_active

def FindCost(arr):
    sum = 0
    for i in range(len(arr)-1):
        temp = z[arr[i]]
        price = temp[arr[i+1]]
        sum+= price
    print("Biaya Perjalanan =",sum) 

def search(start,end):
    i = 0
    p.append(start)
    while(True):
        generate(start)
        start = constructing()
        if (start == end):
            fin = pathfinder(end,p)
            print("Jalur yang ditemukan =",fin)
            FindCost(fin)
            break
       

search(0,3)

G = nx.Graph()
nodes = ["rumah","matos","sma","transmart","um"]
weighted_edges = [
    ("rumah", "matos", 0.55), ("rumah", "sma", 0.65),
    ("matos", "transmart", 0.4), ("matos", "um", 0.95),
    ("sma", "um", 0.7), 
]


G.add_nodes_from(nodes)
G.add_weighted_edges_from(weighted_edges)

options = {
    'node_color': 'orange',
    'node_size': 300,
    'width': 1,
}

print(list(G.nodes))
print(list(G.edges))
for n, nbrs in G.adj.items():
    for nbr, eattr in nbrs.items():
        wt = eattr['weight']
        if wt > 0: print(f"({n}, {nbr}, {wt})")

nx.draw(G, with_labels=True, font_weight='normal', **options)
plt.show()

