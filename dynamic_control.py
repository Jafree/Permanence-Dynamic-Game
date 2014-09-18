'''
Created on 9 18 2014

@author: Fei Jiang
'''
import os
import graph

def dynamic_control(dirpath,outdirpath,initial = "restart"):
    '''
        Input:  a path for a folder as dirpath
                a path for output as outdirpath
                three strategy to choose in restart, resume, penalty as initial
        Output: The analysis of the
    '''
    
    last_graph = None          
    last_community_result = None   
    "Store the graph list and community result from last snapshot"
    for infile in os.listdir(dirpath):  
        "For each snapshot"
        if not os.path.isfile(dirpath + "/" +infile):
            continue
        "Set up the graph list"
        cur_graph = graph(dirpath + "/" +infile)
        "Run community detection on current graph using last graph and initializing strategy"
        cur_community_result = cur_graph.permanence_modularity_community(initial,last_graph,last_community_result)
        
        '''
            TODO:
            Do some calculation here.
            For example, compute modularity, permanence, conductance of the graph with community result.
        '''
        
        
        
        "Have processed current snapshot yet, we will move to next snapshot."
        last_graph = cur_graph
        last_community_result = cur_community_result


if __name__ == '__main__':
    "Input: a path for a folder"
    dirpath = raw_input("Please enter the path of a folder under which the snapshots will be analyzed:\n")
    if not os.path.isdir(dirpath):
        print "The input is not a directory!"
        return False
    "Set a output folder"
    outdirpath = dirpath + "/output"
    if not os.path.isdir(outdirpath):
        os.mkdir(outdirpath)
    dynamic_control(dirpath,outdirpath)
    
    
    '''
        TODO:
        Do some analysis and plot 
    '''
    
    
    
    
    