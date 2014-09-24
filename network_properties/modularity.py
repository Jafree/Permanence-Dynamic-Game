'''
Created on 2014/9/22

@author: Fei Jiang
@email: fei.jiang1989@gmail.com
'''
from collections import defaultdict
def modified_modularity_node(g,node_v):
    '''
    The input graph is undirected, unweighted graph.
    This function is used for calculating the modularity of a node in overlapping community structure.
    The modularity of a node in an overlapping community is its modularity in each community.
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
    The output is the modified modularity of a node
    '''
    modularity = 0
    edge_count = g.edge_count
    "Store the neighboring set of node_v"
    neighbor_set = g.graphlist[node_v]
    "The degree of node_v"
    degree_v = len(neighbor_set)
    "A dict for store the community and its respective members in node_v's neighbors"
    neighbor_community_set = defaultdict(set)
    for node in neighbor_set:
        for community in g.node_map_to_community[node]:
            neighbor_community_set[community].add(node)
    
    """
    Compute the max external community for selecting, we only need to select first two community with 
    largest external edges
    """
    
    for community in g.node_map_to_community[node_v]:
        "Get the inner node set of current community for node_v"
        inner_node_set = neighbor_set.intersection(g.community_map_to_node[community])
        "Get the internal edges number"
        inner_node_count = len(inner_node_set)
        "Get the external node set"
        external_node_set = neighbor_set - inner_node_set
        community_number_dict = defaultdict(lambda: 0)
        for node_e in external_node_set:
            for community_e in g.node_map_to_community[node_e]:
                community_number_dict[community_e] += 1
        if len(community_number_dict)==0:
            e_max = (-1,0)
        else:
            """
            TODO:
            Problems?
            """
            e_max = max(community_number_dict.iteritems(),key=lambda x:x[1])
        "For each community of node_v, compute the modified modularity"
        modularity_for_current_community = 0
        
        "Compute the internal modularity for node_v"
        for node_i in g.community_map_to_node[community]:
            modularity_for_current_community = modularity_for_current_community + 1 - (degree_v * len(g.graphlist[node_i]))/ float(2 * edge_count) \
            if node_i in neighbor_set else modularity_for_current_community - (degree_v * len(g.graphlist[node_i]))/ float(2 * edge_count)
        "Compute the external modularity for node_v"
        "----Debug--"
        """_____Problem TODO:
        Condition:aLl the edges are internal
        """
        if e_max[0] != -1:
            for node_i in neighbor_set:
                if node_i in g.community_map_to_node[e_max[0]]:
                    modularity_for_current_community = modularity_for_current_community - (1 - (degree_v * len(g.graphlist[node_i]))/ float(2 * edge_count)) 
                    """
                    else modularity_for_current_community + (degree_v * len(g.graphlist[node_i]))/ float(2 * edge_count)
                    """
        modularity += modularity_for_current_community/ float(inner_node_count + e_max[1])
    
    return modularity


def modularity(g):
    '''
    This function is used for calculating the modularity of a graph which in defined by Newman
    in overlapping community structure.
    The input graph is undirected, unweighted graph.
    The modularity of a node in an overlapping community is its modularity in each community.
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
    The output is the modularity of the graph
    '''
    modularity = 0
    if(len(g.community_map_to_node) == 1):
        return 0
    edge_count = g.edge_count
    for community in g.node_map_to_community[1]:
        "W.r.t each community, calculate the modularity"
        node_set_in_community = g.community_map_to_node[community]
        for node_i in node_set_in_community:
            "For each node in the community"
            neighbor_set = g.graphlist[node_i]
            degree_node_i = len(neighbor_set)
            for node_j in node_set_in_community: 
                "For each node in the community"
                if(node_i == node_j):
                    continue      
                modularity = modularity - degree_node_i * len(g.graphlist[node_j])/float(2*edge_count) + 1 \
                if node_j in neighbor_set else modularity - degree_node_i * len(g.graphlist[node_j])/float(2*edge_count)
    return modularity / float(2 * edge_count)
                    
