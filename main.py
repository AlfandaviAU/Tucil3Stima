import networkx as nx
import matplotlib.pyplot as plt
from math import radians, cos, sin, asin, sqrt
import os
os.system('cls')


place = []
koordinat = []
active = []
asu = []
heu = []
cost = []
possibilities = []

def conv(x):
    res = {}
    for i in range(len(x)):
        val = {}
        for j in range(len(x)):
            if (float(x[i][j]) != 0):
                val_key = j
                val_value = float(x[i][j])
                val[val_key] = val_value
        key = i
        res[key] = val
    
    return res

def getListKey(a, graph): # ambil key
    return list(graph[a].keys())

def readLoc(file):
    with open(file) as f:
        content = f.readlines()
    for i in content:
        x = i.replace('\n','')
        y = x.split('	')
        z = y[1].split(', ')
        place.append(y[0])
        koordinat.append(z)
    
    for i in koordinat:
        for j in range(len(i)):
            temp = float(i[j])
            i[j] = temp

def readCon(file):
    with open(file) as f:
        content = f.readlines()
    res = []
    for i in content:
        x = i.replace('\n','')
        y = x.split(' ')
        res.append(y)
    pathhasilnyaderBerjarak(res)
    return res

def pathhasilnyaderBerjarak(arr):
    for i in range(len(arr)):
        for j in range(len(arr[i])):
            if (arr[i][j] == '1'):
                arr[i][j] = harvesine(koordinat[i],koordinat[j])
            else :
                arr[i][j] = 0

def uiBiasalah():
    print("Index       Places                          Coordinates")
    for i in range(len(place)):
        num1 = len("Kode        ")
        num2 = len("place                          ")
        print(i," "*(num1 - len(str(i)) - 1),end="")
        print(place[i]," "*(num2 - (len(place[i])) - 1),end="")
        print(koordinat[i][0]," , ",koordinat[i][1])

def harvesine(point1, point2):
    temp1 = radians(point2[1]) - radians(point1[1]) 
    temp2 = radians(point2[0]) - radians(point1[0])
    temp3 = sin(temp2 / 2)**2 + cos(radians(point1[0])) * cos(radians(point2[0])) * sin(temp1 / 2)**2
    temp4 = 2 * asin(sqrt(temp3)) 
    return(temp4 * 6371000) # jari-jari bumi

def heuristicgen(dest):
    for i in koordinat:
        heu.append(harvesine(koordinat[dest],i))




def minimum(array) :
    minimal = array[0]
    idx = 0
    for i in range(1,len(array)):
        if (array[i] < minimal):
            minimal = array[i]
            idx = i 
    return idx


def getPath(x,arr):
    if (len(arr) == 1):
        return list(arr)
    else :
        for i in range(len(arr)):
            if (arr[i][len(arr[i]) - 1] == x):
                temp = list(arr[i])
        return temp

def getActive_Cost(a,graph):
    temp = dict(graph[a])
    for i in (graph[a].keys()):
        active.append(i)
        x = temp[i] + heu[i]
        cost.append(x)



def cariPath(list_key,arr):
    temp = []
    for i in range(len(list_key)):
        temp.append(list(arr))
        temp[i].append(list_key[i])
    return temp

def remove(x):
    if (len(asu) == 1):
        asu.pop(0)
    else :
        for i in range(len(asu)):
            if (asu[i] == x):
                asu.pop(i)

def generate(x):
    getActive_Cost(x,bobot)
    key = getListKey(x,bobot)
    path = getPath(x,asu)
    temp = cariPath(key,path)
    remove(path)
    for i in temp:
        asu.append(i)

def construct():
    idx = minimum(cost)
    new_active = active[idx]
    active.pop(idx)
    cost.pop(idx)
    return new_active

def estimasiJarak(arr):
    sum = 0
    for i in range(len(arr)-1):
        temp = bobot[arr[i]]
        dist = temp[arr[i+1]]
        sum += dist
    print("Jarak yang ditempuh : ",sum," meter") 

def Astar(start,end):
    i = 0
    heuristicgen(end)
    asu.append(start)
    while(True):
        generate(start)
        start = construct()
        if (start == end):
            hasilnya = getPath(end,asu)
            print("Rute yang akan ditempuh : ")
            for i in range (len(hasilnya)):
                if (i != 0):
                    print(" -> " + str(hasilnya[i]),end="")
                else:
                    print(hasilnya[i],end="")
            print("\n")
            estimasiJarak(hasilnya)
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
    plt.uiBiasalah()

readlocf = ""
readconf = ""
print("GOOGLE MAPS FAKE \n")
print("Choose Test Case")
print("1")
print("2")
print("3")
print("4")
x = '0'
while(x < '1' or x > '4'):
    x = input()
    if(x == '1'):
        readlocf = "testCase/loc1.txt"
        readconf = "testCase/con1.txt"
        
    if(x == '2'):
        readlocf = "testCase/loc2.txt"
        readconf = "testCase/con2.txt"
        
    if(x == '3'):
        readlocf = "testCase/loc3.txt"
        readconf = "testCase/con3.txt"

    if(x == '4'):
        readlocf = "testCase/loc4.txt"
        readconf = "testCase/con4.txt"
        
print("HERE'S UR DATA \n ")
print("======================= DATABASE =====================================================")
readLoc(readlocf)
x1 = readCon(readconf)
bobot = conv(x1)
uiBiasalah()
print("======================================================================================")
init = int(input("MULAI DARI : "))
dest = int(input("BERHENTI DI : "))

# Proses Utamanya
Astar(init,dest) # panggil fungsinya
