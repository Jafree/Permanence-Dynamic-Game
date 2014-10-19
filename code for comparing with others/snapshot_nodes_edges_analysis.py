'''
Created on 9 18 2014

@author: Fei Jiang
@contact: fei.jiang1989@gmail.com
'''
import os
import graph
import datetime
from network_properties import *

def nodes_edges_analysis(dirpath,outdirpath):
    '''
        Input:  a path for a folder as dirpath
                a path for output as outdirpath
                three strategy to choose in restart, resume, penalty as initial
        Output: The analysis of the
    '''
    "Check the input and output folders"
    if not os.path.isdir(dirpath):
        print "The input is not a directory!"
        return False
    if not os.path.isdir(outdirpath):
        os.mkdir(outdirpath)
    
    last_graph = None      
    node_numbers = []
    edge_numbers = []
    node_change_numbers = []
    edge_change_numbers = []
    "Store the graph list and community result ([0]node to community and [1]community to node) from last snapshot"
    for infile in os.listdir(dirpath):  
        "For each snapshot"
        if not os.path.isfile(dirpath + "/" +infile):
            continue
        "Set up the graph list"
        print dirpath + "/" +infile
        cur_graph = graph.graph(dirpath + "/" +infile)
        node_numbers.append(cur_graph.node_count)
        edge_numbers.append(cur_graph.edge_count)
        if last_graph == None:
            node_change_numbers.append(cur_graph.node_count)
            edge_change_numbers.append(cur_graph.edge_count)
        else:
            cur_node_set = set(cur_graph.graphlist.iterkeys())
            last_node_set = set(last_graph.graphlist.iterkeys())
            common_node_set = cur_node_set.intersection(last_node_set)
            node_change_numbers.append(len(cur_node_set - common_node_set)+len(last_node_set-common_node_set))
            
            common_edge_number = 0
            for node_i in common_node_set:
                for node_j in common_node_set:
                    if cur_graph.is_edge_exists(node_i, node_j) and last_graph.is_edge_exists(node_i,node_j):
                        common_edge_number +=1
            edge_change_numbers.append(cur_graph.edge_count - common_edge_number/2)
            
        "Have processed current snapshot yet, we will move to next snapshot."
        last_graph = cur_graph
    f = open(outdirpath+"/analysis_nodes_edges.txt","w")
    for i in xrange(0,733):
        f.write(str(node_numbers[i])+" "+str(edge_numbers[i])+" "+str(node_change_numbers[i])+\
        " "+str(edge_change_numbers[i])+"\n")
    f.close()
if __name__ == '__main__':
    "Input: a path for a folder"
    dirpath = raw_input("Please enter the path of a folder under which the snapshots will be analyzed:\n")
    
    "Set a output folder"
    outdirpath = dirpath + "/output"
    
    nodes_edges_analysis(dirpath,outdirpath)
    
    print "Done!"
    
    
    
    