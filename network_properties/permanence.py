'''
Created on 9 19 2014

@author: Fei Jiang
@contact: fei.jiang1989@gmail.com
'''
from collections import defaultdict
def permanence_node(g,node_v):
    """
    The input graph is undirected, unweighted graph.
    This function is used for calculating the permanence of a node in overlapping community structure.
    The permanence of a node in overlapping community structure is its permanence in each community.
    The inputs are the graph class and community result which is a tuple consisting of two dictionaries
    as node to community, community to node.
    The format of community_result is as follows:
    (
        {
            1 : set([1,2]),
            3 : set([2])
        },
        {
            1 : set([1]),
            2 : set([1,3])
        }
    )
    The output is the permanence of node_v
    """
    "Judge the except scenario"
    """
    if not isinstance(g,graph.graph):
        print "Input a wrong parameter to function permanence_node, see detail in document of the function"
        return None
    """
    if node_v not in g.graphlist.iterkeys():
        print "There isn't a node %d in the graph" % node_v
        return None
    
    "TODO: Check the correctness for community_set"
    community_set = g.node_map_to_community[node_v]
    "When node_v is in a singleton community, permanence is zero"
    if len(community_set) == 1 and len(g.community_map_to_node[list(community_set)[0]]) == 1:
        return 0
    "Initialization for the permanence"
    permanence_sum = 0
    "neighbor set of node v"
    neighbor_set = g.graphlist[node_v]
    degree_node_v = len(neighbor_set)
    for community in community_set:
        "Initialization the inner edges for each community"
        inner_edges = 0
        
        "When E_max=0, permanence of node_v is its clustering coefficient inside the community."
        if neighbor_set.issubset(g.community_map_to_node[community]):
            for node_i in neighbor_set:
                for node_j in neighbor_set:
                    if g.is_edge_exists(node_i,node_j):
                        inner_edges += 1
            "Debug  TODO:"
            if len(neighbor_set) <= 2:
                "The nodes in community is less than 2, clustering is 0"
                "Debug: TODO:"
                clustering_coefficient = 1 
                "clustering_coefficient = 0" 
            else:
                "Otherwise, do computation"
                clustering_coefficient = inner_edges /float( len(neighbor_set) * (len(neighbor_set)-1) )
            permanence_sum += clustering_coefficient
            continue
        "The nodes inside the community and neighboring node_v"
        inner_node_set = neighbor_set.intersection(g.community_map_to_node[community])
        
        "Compute the max number of the external node in a community"
        external_node_set = neighbor_set - inner_node_set
        community_number_dict = defaultdict(lambda: 0)
        for node_e in external_node_set:
            for community_e in g.node_map_to_community[node_e]:
                community_number_dict[community_e] += 1
        e_max = max(community_number_dict.itervalues())
        
        "When the number of neighboring nodes is less than two, the clustering coefficient is zero"
        "TODO:debug"
        if len(inner_node_set) <= 2 and len(inner_node_set)>e_max:
            clustering_coefficient = 1
        elif len(inner_node_set) <= 2:
            clustering_coefficient = 0
        else:
            "Otherwise, compute the clustering coefficient"
            for node_i in inner_node_set:
                for node_j in inner_node_set:
                    if g.is_edge_exists(node_i,node_j):
                        inner_edges += 1
            clustering_coefficient = inner_edges /float( len(inner_node_set) * (len(inner_node_set)-1) )
        
        permanence_sum += (len(inner_node_set) / float(e_max * degree_node_v) - 1 + clustering_coefficient)
    return permanence_sum
        
def permanence(g):
    '''
    The input graph is undirected, unweighted graph.
    This function is used for calculating the permanence of a graph in overlapping community structure.
    The permanence of a node in an overlapping community is its permanence in this community.
    The inputs are the graph class and community result which is a tuple consisting of two dictionaries
    as node to community, community to node.
    The format of community_result is as follows:
    (
        {
            1 : set([1,2]),
            3 : set([2])
        },
        {
            1 : set([1]),
            2 : set([1,3])
        }
    )
    The output is the permanence of the graph
    '''
    permanence_sum = 0
    for node_v in g.graphlist.iterkeys():
        permanence_sum += permanence_node(g,node_v)
    return permanence_sum / sum(len(g.node_map_to_community[neighboring_node]) for neighboring_node in g.graphlist.iterkeys())
    
    
    
    
    
    
    
    