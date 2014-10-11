from collections import defaultdict
def permanence_node_igraph(g,clustering,node_v):
    '''
    This function is used for calculating the permanence of community result w.r.t a vertex.
    The input will be igraph classes Graph and VertexClustering,Vertex.
    '''
    if node_v not in g.vs:
        print "There isn't a node %d in the graph" % node_v
        return None
    community_v = clustering.membership[node_v.index]
    "When node_v is in a singleton community, permanence is zero"
    if len(clustering[community_v])==1:
        return 0
    "Initialization for the permanence"
    permanence = 0
    "neighbor set of node v"
    neighbor_list = node_v.neighbors()
    degree_v = node_v.degree()
    "Initialization the inner edges for each community"
    inner_edges = 0
        
    
    e_max_exist_test = False 
    for node in neighbor_list:
        "Test whether there is external edges"
        if node.index not in clustering[community_v]:
            e_max_exist_test = True 
            break
    "When E_max=0, permanence of node_v is its clustering coefficient inside the community." 
    if e_max_exist_test == False:
        for node_i in neighbor_list:
            for node_j in neighbor_list:
                if node_i in node_j.neighbors() or node_j in node_i.neighbors():
                    inner_edges += 1
        "Debug  TODO:"
        if len(neighbor_list) <= 2:
            "The nodes in community is less than 2, clustering is 0"
            "Debug: TODO:"
            clustering_coefficient = 1
            "clustering_coefficient = 0" 
        else:
            "Otherwise, do computation"
            clustering_coefficient = inner_edges /float( len(neighbor_list) * (len(neighbor_list)-1) )
        permanence = clustering_coefficient
    
    else:
        "When E_max != 0"
        "The nodes inside the community and neighboring node_v"
        inner_node_list = []
        external_node_list = []
        for node in neighbor_list:
            if node.index in clustering[community_v]:
                inner_node_list.append(node)
            else:
                external_node_list.append(node)  
        community_number_dict = defaultdict(lambda: 0)
        for node_e in external_node_list:
            community_number_dict[clustering.membership[node_e.index]] += 1
        e_max = max(community_number_dict.itervalues())
        
        "When the number of neighboring nodes is less than two, the clustering coefficient is zero"
        "TODO:debug"
        if len(inner_node_list) <= 2 and len(inner_node_list)>len(external_node_list):
            clustering_coefficient = 1
        elif len(inner_node_list) <= 2:
            clustering_coefficient = 0
        else:
            "Otherwise, compute the clustering coefficient"
            for node_i in inner_node_list:
                for node_j in inner_node_list:
                    if node_i in node_j.neighbors() or node_j in node_i.neighbors():
                        inner_edges += 1
            clustering_coefficient = inner_edges /float( len(inner_node_list) * (len(inner_node_list)-1) )
        
        permanence = len(inner_node_list) / float(e_max * degree_v) - 1 + clustering_coefficient
        """
        print "Emax=",e_max,"degree_v=",degree_v,"inner_node=",len(inner_node_list),"clusteringcoe=",clustering_coefficient
        """
    return permanence

def permanence_igraph(g,clustering):
    '''
    This function is used for calculating the permanence of community result.
    The input will be igraph classes Graph and VertexClustering.
    '''
    permanence_sum = 0
    for node_v in g.vs:
        permanence_sum += permanence_node_igraph(g,clustering,node_v)
    return permanence_sum / float(g.vcount())