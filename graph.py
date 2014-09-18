'''
Created on 2014/9/18

@author: free
'''
from collections import defaultdict
class graph:
    '''
    This class is used for storing a undirected  unweighted graph from the input file.
    The format of the input file should be the edge list in lines, such as:
    #example
    SourceNode \t TargetNode
    
    '''


    def __init__(self, filepath="as19971108.txt"):
        '''
        Constructor
        '''
        self.filepath = filepath
        self.store_graphlist()
        print "processing %s" % self.filepath
    
    def store_graphlist(self):
        '''
        Store the adjacency list in dictionary, such as
        {
         1 : set([2,3,9]),
         19: set([3,6,7])
        }
        '''
        self.graphlist = defaultdict(set)
        current_file = open(self.filepath)
        for line in current_file:
            if line[0] != "#" and len(line)>1:
                linepair = map(int,line.rstrip().split("\t"))
                self.graphlist[linepair[0]].add(linepair[1])
                self.graphlist[linepair[1]].add(linepair[0])
        "Store the node count and edge count"
        self.node_count = len(self.graphlist)
        self.edge_count = sum([len(self.graphlist[i]) for i in self.graphlist])/2
        current_file.close()
        "print self.graphlist"
    
    def is_node_exists(self,node_v):
        '''
            Return if a node_v exits in the graph
        '''
        if node_v in self.graphlist:
            return True
        return False
        
    def neighboring_node(self,node_v):
        '''
            Yield an iterator for the neighbor of node_v 
        '''
        for node_i in self.graphlist[node_v]:
            yield node_i 
    
    def is_edge_exists(self,node_i,node_j):
        '''
            Return if an edge exists between node_i and node_j
        '''
        if node_i in self.graphlist[node_j]:
            return True
        return False
    
    def permanence_modularity_community(self,initial,last_graph,last_community_result):
        '''
            TODO:
            Realization
        '''
        if initial == "restart" or (last_graph == None):
            pass
        
        if initial == "resume":
            pass
        
        if initial == "penalty":
            pass    
    
    
    
    
    
    
    
    
    
    
    
        
        
        
        
        
        
        
        
        
        