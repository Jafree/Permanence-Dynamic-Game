'''
Created on 9 18 2014

@author: Fei Jiang
@contact: fei.jiang1989@gmail.com
'''
import os
import graph
import datetime
from network_properties import *

def dynamic_control(dirpath,outdirpath,initial = "resume",select = "random",penalty = 0.5):
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
    time_cost = []
    perm = []
    modu = []
    community_number = []
    max_community_size = []
    average_commmunity_size = []    
    "Store the graph list and community result ([0]node to community and [1]community to node) from last snapshot"
    for infile in os.listdir(dirpath):  
        "For each snapshot"
        if not os.path.isfile(dirpath + "/" +infile):
            continue
        "Set up the graph list"
        print dirpath + "/" +infile
        cur_graph = graph.graph(dirpath + "/" +infile)
        "Run community detection on current graph using last graph and initializing strategy"
        starttime = datetime.datetime.now()
        cur_graph.permanence_modularity_community(last_graph,initial,select)
        endtime = datetime.datetime.now()
        time_cost.append((endtime-starttime).seconds)
        perm.append(permanence.permanence(cur_graph))
        modu.append(modularity.modularity(cur_graph))
        community_number.append(len(cur_graph.community_map_to_node))
        max_community_size.append(max(len(members) for members in cur_graph.community_map_to_node.itervalues()))
        average_commmunity_size.append(sum(len(members) for members in cur_graph.community_map_to_node.itervalues())/float(len(cur_graph.community_map_to_node)))
        
        '''
            TODO:
            Do some calculation here.
            For example, compute modularity, permanence, conductance of the graph with community result.
        '''
        "Have processed current snapshot yet, we will move to next snapshot."
        last_graph = cur_graph
    f = open(outdirpath+"/analysis.txt","w")
    for i in xrange(len(time_cost)):
        f.write(str(time_cost[i])+" "+str(perm[i])+" "+str(modu[i])+\
        " "+str(community_number[i])+" "+str(max_community_size[i])+" "+str(average_commmunity_size[i])+"\n")
    f.close()
if __name__ == '__main__':
    "Input: a path for a folder"
    dirpath = raw_input("Please enter the path of a folder under which the snapshots will be analyzed:\n")
    
    "Set a output folder"
    outdirpath = dirpath + "/output"
    
    dynamic_control(dirpath,outdirpath,penalty=0.5)
    
    
    '''
        TODO:
        Do some analysis and plot 
    '''
    
    
    
    
    