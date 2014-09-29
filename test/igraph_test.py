'''
Created on 2014/9/29

@author: free
'''
from igraph import Graph
g = Graph.Read_Edgelist("../as19971108_only_edge.txt", directed=False)
community_1 = g.community_infomap()
'community_2 = g.community_walktrap()'

print g.modularity(community_1)
"print g.modularity(community_2)"


"print community"