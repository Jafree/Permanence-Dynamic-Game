'''
Created on 9 18 2014

@author: Fei Jiang
@contact: fei.jiang1989@gmail.com
'''
import os
import graph
import datetime
from network_properties import *

def cluster_analysis(dirpath,outdirpath):
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
    time_cost = [] 
    perm = []
    modu = []
    community_number = []
    max_community_size = []
    average_commmunity_size = []
    membership_pool = []
    for i in xrange(1,734):
            membership_pool.append("E:/9_Dataset/Evolving_Network/as-733/community_node_outputs_labelrankT/syn_LabelRankT_"+str(i)+"_D0_W0_S1_POWER1_THR0.1_I4_MTHR0.6_RST200.icpm")
    file_count = 0
    "Store the graph list and community result ([0]node to community and [1]community to node) from last snapshot"
    for infile in os.listdir(dirpath):  
        "For each snapshot"
        if not os.path.isfile(dirpath + "/" +infile):
            continue
        "Set up the graph list"
        print dirpath + "/" +infile
        cur_graph = graph.graph(dirpath + "/" +infile)
        "Run community detection on current graph using last graph and initializing strategy"
        f_cluster = open(membership_pool[file_count])
        print membership_pool[file_count]
        file_count += 1
        cluster_count = 0
        for line in f_cluster:
            if len(line)!="\n":
                members = set(map(int,line.rstrip().split()))
                cur_graph.community_map_to_node[cluster_count] = members
                for member in members:
                    cur_graph.node_map_to_community[member] = {cluster_count}
                cluster_count+=1
        """
        print len(cur_graph.graphlist)
        print len(cur_graph.node_map_to_community)
        print cur_graph.node_map_to_community
        print cur_graph.community_map_to_node
        """
        time_cost.append(0)
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
    f = open(outdirpath+"/analysis_labelrankT.txt","w")
    for i in xrange(len(time_cost)):
        f.write(str(time_cost[i])+" "+str(perm[i])+" "+str(modu[i])+\
        " "+str(community_number[i])+" "+str(max_community_size[i])+" "+str(average_commmunity_size[i])+"\n")
    f.close()
if __name__ == '__main__':
    "Input: a path for a folder"
    dirpath = raw_input("Please enter the path of a folder under which the snapshots will be analyzed:\n")
    
    "Set a output folder"
    outdirpath = dirpath + "/output"
    cluster_analysis(dirpath,outdirpath)
    
    print "Done!"
    '''
        TODO:
        Do some analysis and plot 
    '''
    
    
    
    
    