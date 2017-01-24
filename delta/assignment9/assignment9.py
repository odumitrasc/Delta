import pandas as pd
import time
import networkx as  nx

store = pd.HDFStore('store2.h5')
df2 = store['df2']
store.close()

numOfVertcies = len(df2['out_links'])

graph = dict()

for i in range(numOfVertcies):
    graph[df2['name'][i]] = df2['out_links'][i]

def diameter(graphs):
    diameters = list()
    for graph in graphs:
        diameters.append(nx.diameter(graph))   
    return max(diameters)

G = nx.Graph(graph)

start = time.time()
connectedComponentsGraphs = list(nx.connected_component_subgraphs(G))
print("Diameter of the Graph is: " + str(diameter(connectedComponentsGraphs)))
end = time.time()

totalTime = end - start

print(totalTime)