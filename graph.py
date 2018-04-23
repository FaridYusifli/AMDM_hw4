
# coding: utf-8

# In[1]:


import json
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import networkx as nx
import heapq
import numpy as np


# In[2]:


# Jaccard's Similarity:
def jaccardSim(data1, data2):
    coauthorList1 = []
    for item in data1:
        key = list(item.keys())[0]
        coauthorList1.append(key)

    coauthorList2 = []
    for item in data2:
        key = list(item.keys())[0]
        coauthorList2.append(key)

    intersect = len(set(coauthorList1).intersection(coauthorList2))
    similarityScore = (intersect / ((len(coauthorList1) + len(coauthorList2)) - intersect))

    return similarityScore


# In[3]:


#Shortest path (Dijkstra)
def Shortest_path(G, start, end):
    if start == end:
        result = 0
    elif nx.has_path(G, start, end):
        neighb = []
        seen = set()
        lis = G[start] #all neighbours of start node(prof.: A.Aris)
        seen.add(start)
        for i in lis:
            heapq.heappush(neighb, (lis[i]['weight'], i))
            #add the neighbours of the input and their weight to heap
        while neighb:
            min_neighb = heapq.heappop(neighb)
            weight = min_neighb[0]
            node = min_neighb[1]
            seen.add(node) 
            if node == end:
                return weight
            node_neighb = G[node]  #take neigbours of neighbour
            for j in node_neighb:   
                if j not in seen:
                    is_in_neighb = False
                    for i in neighb:
                        if i[1] == j:
                            min_dist = min(i[0], node_neighb[j]['weight'] + weight)
                            #take minimum between input's neighbour and input's neighbours' neighbour
                            is_in_neighb = True
                            neighb.remove(i)
                            heapq.heappush(neighb, (min_dist, j))
                            break
                    if is_in_neighb == False:
                        heapq.heappush(neighb, (node_neighb[j]['weight'] + weight, j))
    else:
        result = float('inf')
    return result


# In[4]:


def group_authors(G, t):
    dic = {}
    for i in G.nodes():
        lst = []
        for j in t:
            if i != j:
                d = Shortest_path(G, i, j)
                if d != float('inf'): #if these 2 nodes are connected
                    lst.append((d, j)) #appent its 'weight' ad 'id' to the list
        try:
            min_dist = heapq.heappop(lst) #take min. weight
            dic[i] = min_dist
            
        except:
            dic[i] = "NaN"
        
    result={}
    
    for k,v in dic.items():
        if v!='NaN': #if 2 nodes has connection
            if v[1] not in result: 
                result[v[1]]=[(k,v[0])] 
            elif v[1] in result:
                result[v[1]].append((k,v[0]))           
        
    return result


# In[5]:


datab = input("Choose the database: (reduced' / 'full') : ")

if datab == "reduced":
    f = open('reduced_dblp.json', 'r')
    data = f.read()
    f.close()
if datab == "full":
    f = open('full_dblp.json', 'r')
    data = f.read()
    f.close()

#reading data from json file
dataset = json.loads(data)
type(dataset)

#Creating myDict:
myDict={}
for dic in range(len(dataset)):
    myList=[]
    confID=dataset[dic]['id_conference_int']
    pubID=dataset[dic]['id_publication_int']
    for j in range(len(dataset[dic]['authors'])):
        authorID=(dataset[dic]['authors'][j]['author_id'])
        myList=[{pubID:confID}]
        if authorID not in myDict:
            myDict[authorID]=myList            
        else:
            myDict[authorID].append({pubID:confID})


# In[6]:


#Creating Graph:
G=nx.Graph()

for data in dataset:
    for author in data["authors"]:
        for author2 in data["authors"]:
            if (author["author_id"] != author2["author_id"]) and (not((G.has_edge(author["author_id"],author2["author_id"])))):
                G.add_node(author["author_id"])
                G.add_node(author2["author_id"])
                edgeWeight= 1-jaccardSim(myDict[author["author_id"]],myDict[author2["author_id"]])
                G.add_edge(author["author_id"],author2["author_id"], weight=edgeWeight)

print(nx.info(G))


# In[10]:


a = input("Enter the number of the exercise you want to run:")
if a == "2a":
    Conferences = {}
    for book in dataset:
        confID = book['id_conference_int']  
        for author in book['authors']:
            authorID = author['author_id']
            if confID not in Conferences.keys():
                Conferences[confID] = []
            else:
                Conferences[confID].append(authorID)
    print(Conferences.keys())

    confID = int(input("Search confID:"))      
    nodeList = []
    for k,v in myDict.items(): #v is the (confID,pubID)..[{161687: 3052}, {383148: 6920}]
        for j in range(len(v)):
            if(list(v[j].values())[0]==confID):
                nodeList.append(k) #list of author (nodes)

    H = G.subgraph(nodeList)
    plt.figure(figsize=(20, 8))
    plt.clf()
    nx.draw(H)
    plt.show()

    # Centrality measures:

    degree_centrality = nx.algorithms.centrality.degree_centrality(H)
    degree_dict={}
    for key, values in degree_centrality.items():
        if values not in degree_dict.keys():        
            degree_dict[values]=1  #count # of degree centrality measure in graph
        else:
            degree_dict[values]+=1 


    closeness_centrality = nx.algorithms.centrality.closeness_centrality(H)
    closeness_dict={}
    for key, values in closeness_centrality.items():
        if values not in closeness_dict.keys():        
            closeness_dict[values]=1
        else:
            closeness_dict[values]+=1

    betweenness_centrality = nx.algorithms.centrality.betweenness_centrality(H)    
    betweenness_dict={}
    for key, values in betweenness_centrality.items():
        if values not in betweenness_dict.keys():        
            betweenness_dict[values]=1
        else:
            betweenness_dict[values]+=1

    def plot(dict,text):
        x = np.arange(len(dict))
        y = [i for i in dict.values()]
        plt.figure(figsize=(20, 8))
        plt.bar(x, y)
        plt.title(text,fontsize=20)
        plt.xticks(x, sorted(("%.5f" % a for a in dict.keys())),rotation=90)
        plt.show()

    plot(degree_dict,text='Degree Centrality')
    plot(closeness_dict,text='Closeness Centrality')
    plot(betweenness_dict,text='Betweenness Centrality')
      
elif a == "2b":
    searchauthorID = int(input("Search authorID: ")) #for example - 256176
    hopDistance=int(input("Enter Hop Distance: "))
    
    test=nx.ego_graph(G, searchauthorID, radius=hopDistance,center=True) 
    plt.figure(figsize=(20, 8))
    plt.clf()
    nx.draw(test)
    plt.show()
   
elif a == "3a":   #79993
    author = int(input("Search the authorID to calculate the shortest path with Aris: "))
    print(Shortest_path(G,256176, author))

elif a == "3b":
     #for example  input = 9503  255902  9070  239007  189237
    t = list(map(int,input("insert a list of authors' ID : ").split()))
    result=group_authors(G, t)
    for k,v in result.items():
        print ('Node {} group : '.format(k))
        print (v,"\n")

else:
    print("Invalid input")

