'''
Created on 2014/9/29

@author: free
'''
from igraph import Graph
g = Graph.Read_Edgelist("../as19971108_only_edge.txt", directed=False)
community_1 = Graph.community_infomap(g)

print g.modularity(community_1)