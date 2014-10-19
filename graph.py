'''
Created on 2014/9/18

@author: Fei Jiang
@contact: fei.jiang1989@gmail.com
'''
from collections import defaultdict
import random
from network_properties import permanence 
from network_properties import modularity 
class graph:
    '''
    This class is used for storing a undirected  unweighted graph from the input file.
    The format of the input file should be the edge list in lines, such as:
    #example
    SourceNode \t TargetNode
    
    '''


    def __init__(self, filepath="KarateTest.txt"):
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
                if line.count("\t")>0:
                    linepair = map(int,line.rstrip().split("\t"))
                elif line.count(" ")>0:
                    linepair = map(int,line.rstrip().split())
                if linepair[0]==linepair[1]:
                    continue
                self.graphlist[linepair[0]].add(linepair[1])
                self.graphlist[linepair[1]].add(linepair[0])
        "Store the node count and edge count"
        self.node_count = len(self.graphlist)
        self.edge_count = sum(len(i) for i in self.graphlist.itervalues())/2
        self.community_map_to_node = defaultdict(set)
        self.node_map_to_community = defaultdict(set)
        self.utility_list = defaultdict(int)
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
    
    def permanence_modularity_community(self,last_graph=None,initial="restart",select="random",penalty=0.5):
        '''
            TODO:
            Realization
        '''
        """
            ----------------------------------------------------------------------------------------
            Initialization for different initial strategies
            ----------------------------------------------------------------------------------------
        """
        self.overlapping_penalty = penalty
        "Each agent belongs to its own community at the initial stage"
        disequilibrium_node_list = defaultdict(int)
        if initial == "restart" or last_graph == None:
            '''
            Store the node to community and community to node in dictionaries, such as
            {
             1 : set([2,3,9]),
             19: set([3,6,7])
             }
            '''
            self.node_map_to_community = {node : {node} for node in self.graphlist.iterkeys()}
            self.community_map_to_node = {node : {node} for node in self.graphlist.iterkeys()}
            "Store the node list for operating"
            disequilibrium_node_list = {node : len(neighbors) for node , neighbors in self.graphlist.iteritems()}
            "Store the utility of each node"
            self.utility_list = {node : self.initial_singleton_community(node)[0] for node in self.graphlist.iterkeys()}
            
            '''
            Each agent belongs to its community in last snapshot if it had exist in last snapshot;
            Otherwise, it will belong to its own singleton community.
            '''
        elif initial == "neighborhood":
            """
            TODO:
            Realization
            """
            
        elif initial == "resume":
            '''
            TODO:
            Realization
            '''
            
            "For nodes exist in both last and current graphs, preserve its community"
            for node,communities in last_graph.node_map_to_community.iteritems():
                if node in self.graphlist.iterkeys():
                    self.node_map_to_community[node] = communities
                    for community in communities:
                        self.community_map_to_node[community].add(node)
                    "If the neighbors are not the exact same, then add it into the disequilibrium_list"
                    if self.graphlist[node] != last_graph.graphlist[node]:
                        disequilibrium_node_list[node] = len(self.graphlist[node])
            "For nodes don't exist in both graphs, create its own community"
            for node in self.graphlist.iterkeys():
                if node not in self.node_map_to_community.iterkeys():
                    singleton_community = node
                    while singleton_community in self.community_map_to_node.iterkeys():
                        singleton_community += 1
                    self.node_map_to_community[node] = {singleton_community}
                    self.community_map_to_node[singleton_community] = {node}
                    "Add the new node into the disequilibrium list"
                    disequilibrium_node_list[node] = len(self.graphlist[node])
            "Calculate the utility for each node"
            for each_node,neighbors in self.graphlist.iteritems():
                utility_each_node = modularity.modified_modularity_node(self, each_node)\
                + permanence.permanence_node(self, each_node)\
                -(len(self.node_map_to_community[each_node])-1)*self.overlapping_penalty
                self.utility_list[each_node] = utility_each_node
                """Add each node into the disequilibrium_node_list
                disequilibrium_node_list[each_node] = len(neighbors)"""
        
        elif initial == "penalty":
            '''
             TODO:
                 The penalty initial will be done
            '''
            pass    
        """
        -------------------------------------------------------------
        Select strategy
        -------------------------------------------------------------
        """
        "Choose a node for the node list if there are nodes in disequilibrium state"
        loop_count = 0
        while len(disequilibrium_node_list) > 0:
            "print len(disequilibrium_node_list)"
            "Random strategy"
            if select == "random":
                "Control the loop number"
                loop_count += 1
                if loop_count >= 10 * self.node_count:
                    break
                selected_node = random.choice(disequilibrium_node_list.keys())
                del disequilibrium_node_list[selected_node]
                "print neighbors=,len(self.graphlist[selected_node])"
            if select == "highdegree":
                "TODO:"
                pass
            if select == "lowdegree":
                "TODO:"
                pass
            if select == "BFS":
                "TODO:"
                pass
            if select == "DFS":
                "TODO:"
                pass
            '''
            -----------------------------------------------
            "Perform the permanence game for selected node"
            -----------------------------------------------
            '''
            """
            Create a singleton community consisting of only one node,singleton_community is
            a community number which is not used by any other community
            
            """
            utility_singleton,singleton_community,utility_neighbors_singleton,utility_total_singleton = self.create_singleton_community(selected_node)
            "Join a new community,join_community = community to be joined"
            utility_join,join_community,utility_neighbors_join,utility_total_join = self.join_a_community(selected_node)
            "Switch a community,switch_community =(community to be switched out, community to be in)"
            utility_switch,switch_community,utility_neighbors_switch,utility_total_switch = self.switch_a_community(selected_node)
            "Leave a community,leave_community = community to be leaved"
            utility_leave,leave_community,utility_neighbors_leave,utility_total_leave = self.leave_a_community(selected_node)
            utility_max = max(\
                              (utility_singleton,singleton_community,utility_neighbors_singleton,utility_total_singleton),\
                              (utility_join,join_community,utility_neighbors_join,utility_total_join),\
                              (utility_switch,switch_community,utility_neighbors_switch,utility_total_switch),\
                              (utility_leave,leave_community,utility_neighbors_leave,utility_total_leave),key=lambda x:x[3])
            
            "If the utility doesn't increase, continue "
            if utility_max[3] <= -20:
                "self.utility_list[selected_node]:"
                continue
            "Otherwise, update the utility value for selected_node's neighbors"
            self.utility_list.update(utility_max[2])
            self.utility_list[selected_node] = utility_max[0]
            "To each scenario, we update the node to community and community to node dictionaries"
            if abs(utility_max[3] - utility_total_switch)<0.0001:
                self.node_map_to_community[selected_node].remove(switch_community[0])
                self.node_map_to_community[selected_node].add(switch_community[1])
                self.community_map_to_node[switch_community[0]].remove(selected_node)
                if len(self.community_map_to_node[switch_community[0]])==0:
                    del self.community_map_to_node[switch_community[0]]
                self.community_map_to_node[switch_community[1]].add(selected_node)
                """Add selected node's neighbors which is in the switch out community or 
                in the switch in community  in the disequilibrium_list"""
                if len(self.node_map_to_community[selected_node])==1:
                    
                    """When switch in only one community, the nodes in switch out community will be include in 
                    the disequilibrium_node_list"""
                    
                    for each_node in self.graphlist[selected_node]:
                        if switch_community[1] not in self.node_map_to_community[each_node]:
                            disequilibrium_node_list[each_node] = len(self.graphlist[each_node])
                else:
                    "Otherwise, every neighbors will be include in the list"
                    for each_node in self.graphlist[selected_node]:
                        disequilibrium_node_list[each_node] = len(self.graphlist[each_node])
            elif abs(utility_max[3] - utility_total_join)<0.0001:
                self.node_map_to_community[selected_node].add(join_community)
                self.community_map_to_node[join_community].add(selected_node)
                """Add selected node's neighbors which is in join in community in the disequilibrium_list"""
                for each_node in self.graphlist[selected_node]:
                    if join_community not in self.node_map_to_community[each_node]:
                        disequilibrium_node_list[each_node] = len(self.graphlist[each_node])
            elif abs(utility_max[3] - utility_total_leave)<0.0001:
                self.node_map_to_community[selected_node].remove(leave_community)
                self.community_map_to_node[leave_community].remove(selected_node)
                if len(self.community_map_to_node[leave_community])==0:
                    del self.community_map_to_node[leave_community]
                """Add selected node's neighbors which is in leave community in the disequilibrium_list"""
                for each_node in self.graphlist[selected_node]:
                    if leave_community in self.node_map_to_community[each_node]:
                        disequilibrium_node_list[each_node] = len(self.graphlist[each_node])
            elif abs(utility_max[3] - utility_total_singleton)<0.0001:
                current_community = self.node_map_to_community[selected_node]
                for each_community in current_community:
                    self.community_map_to_node[each_community].remove(selected_node)
                    if len(self.community_map_to_node[each_community])==0:
                        del self.community_map_to_node[each_community]
                self.node_map_to_community[selected_node] = {singleton_community}
                self.community_map_to_node[singleton_community] = {selected_node}
                """Add selected node's neighbors which is in any before joined community
                in the disequilibrium_list"""
                for each_node in self.graphlist[selected_node]:
                    for each_community in current_community:
                        if each_community in self.node_map_to_community[each_node]:
                            disequilibrium_node_list[each_node] = len(self.graphlist[each_node])
                            break
            """
            "Update the utility for each node in the neighbor set"
            for each_node in self.graphlist[selected_node]:
                self.utility_list[each_node] = \
                permanence.permanence_node(self, each_node)+\
                modularity.modified_modularity_node(self, each_node)-\
                (len(self.node_map_to_community[each_node])-1)*self.overlapping_penalty
                "disequilibrium_node_list[each_node] = len(self.graphlist[each_node])"
            """  
        return True
    
    
    
    def initial_singleton_community(self,selected_node):
        "Find the community number that is not used by any other communities"
        if selected_node in self.node_map_to_community.iterkeys():
            singleton_community = selected_node + 1
            while True:
                if singleton_community not in self.community_map_to_node:
                    break
                else:
                    singleton_community += 1
        else:
            singleton_community = selected_node
        "Calculate the utility for create a singleton_community"
        "Change to calculate"
        current_community_set = self.node_map_to_community[selected_node]
        for each_community in current_community_set:
            self.community_map_to_node[each_community].remove(selected_node)
        self.node_map_to_community[selected_node] = {singleton_community}
        self.community_map_to_node[singleton_community] = {selected_node}
        "Calculation" 
        utility_singleton = modularity.modified_modularity_node(self,selected_node)
        "recover"
        self.node_map_to_community[selected_node] = current_community_set
        
        del self.community_map_to_node[singleton_community]
        
        for each_community in current_community_set:
            self.community_map_to_node[each_community].add(selected_node)
        return utility_singleton,singleton_community
    
    def create_singleton_community(self,selected_node):
        "Find the community number that is not used by any other communities"
        if self.utility_list[selected_node]>=0 or (len(self.node_map_to_community[selected_node])==1 and\
        len(self.community_map_to_node[list(self.node_map_to_community[selected_node])[0]])==1):
            return -100,-100,{},-100
        if selected_node in self.node_map_to_community.iterkeys():
            singleton_community = selected_node + 1
            while True:
                if singleton_community not in self.community_map_to_node:
                    break
                else:
                    singleton_community += 1
        else:
            singleton_community = selected_node
        "Calculate the utility for create a singleton_community"
        "Change to calculate"
        current_community_set = self.node_map_to_community[selected_node]
        for each_community in current_community_set:
            self.community_map_to_node[each_community].remove(selected_node)
        self.node_map_to_community[selected_node] = {singleton_community}
        self.community_map_to_node[singleton_community] = {selected_node}
        "Calculation" 
        utility_singleton = modularity.modified_modularity_node(self,selected_node)
        "Calculate the utility for the neighbors"
        utility_neighbors_singleton = utility_singleton
        utility_neighbors_now = self.utility_list[selected_node]
        utility_neighbors_dict = {}
        for each_node in self.graphlist[selected_node]:
            utility_each_node = modularity.modified_modularity_node(self, each_node)\
            + permanence.permanence_node(self, each_node)\
            -(len(self.node_map_to_community[each_node])-1)*self.overlapping_penalty
            utility_neighbors_singleton += utility_each_node
            utility_neighbors_now += self.utility_list[each_node]
            utility_neighbors_dict[each_node] = utility_each_node
        "recover"
        self.node_map_to_community[selected_node] = current_community_set
        
        del self.community_map_to_node[singleton_community]
        
        for each_community in current_community_set:
            self.community_map_to_node[each_community].add(selected_node)
        "Judge whether the utility of all neighbors increase"
        if utility_neighbors_now >= utility_neighbors_singleton:
            return -100,-100,{},-100
        return utility_singleton,singleton_community,utility_neighbors_dict,utility_neighbors_now
        
    def join_a_community(self,selected_node):
        
        current_community_set = self.node_map_to_community[selected_node]
        """Three overlapping communities are not allowed, and when the utility of community now is
        less than the overlapping penalty, join strategy cannot be applied
        """
        if len(current_community_set)>= 2 or self.utility_list[selected_node]<self.overlapping_penalty:
            return -100,-100,{},-100
        penalty = (len(current_community_set)+1 -1)*self.overlapping_penalty
        "join_community_set = set({})"
        "The community with neighboring number"
        join_community_dict = defaultdict(lambda:0)
        neighbors_in_community_number = 0
        "Find communities to join"
        for each_node in self.graphlist[selected_node]:
            for each_community in self.node_map_to_community[each_node]:
                if each_community not in current_community_set:
                    "join_community_set.add(each_community)"
                    join_community_dict[each_community]+=1
                else:
                    neighbors_in_community_number += 1
        "When the selected_node and its neighbors are in the same community"
        if len(join_community_dict)==0:
            return -100,-100,{},-100
        "Calculate the utility of each community to join in "
        max_community = -100
        max_utility = -100
        utility_neighbors_dict = {}
        utility_neighbors_dict_final ={}
        utility_neighbors_now = self.utility_list[selected_node]
        for each_node in self.graphlist[selected_node]:
            utility_neighbors_now += self.utility_list[each_node]
        max_community_number = max(join_community_dict.itervalues())
        if neighbors_in_community_number >= 2*max_community_number:
            return -100,-100,{},-100
        if max_community_number == 1:
            join_community_set = self.node_map_to_community[min(self.graphlist[selected_node], key=lambda x: len(self.graphlist[x]))]
        join_community_set = {x for x,y in join_community_dict.iteritems() if y==max_community_number}
        for a_community in join_community_set:
            self.node_map_to_community[selected_node].add(a_community)
            self.community_map_to_node[a_community].add(selected_node)
            
            utility_modularity = modularity.modified_modularity_node(self,selected_node)
            utility_permanence = permanence.permanence_node(self,selected_node)
            utility_join = utility_modularity + utility_permanence - penalty
            
            "Calculate the utility for the neighbors"
            utility_neighbors_join = utility_join
            for each_node in self.graphlist[selected_node]:
                utility_each_node = modularity.modified_modularity_node(self, each_node)\
                + permanence.permanence_node(self, each_node)\
                -(len(self.node_map_to_community[each_node])-1)*self.overlapping_penalty
                utility_neighbors_join += utility_each_node
                utility_neighbors_dict[each_node] = utility_each_node
            
            self.node_map_to_community[selected_node].remove(a_community)
            self.community_map_to_node[a_community].remove(selected_node)
            if utility_neighbors_join >= utility_neighbors_now:
                utility_neighbors_now = utility_neighbors_join
                max_utility = utility_join
                max_community = a_community
                utility_neighbors_dict_final.update(utility_neighbors_dict)
        if len(utility_neighbors_dict_final)==0:
            return -100,-100,{-1,-1},-100
        return max_utility,max_community,utility_neighbors_dict_final,utility_neighbors_now
    
    def switch_a_community(self,selected_node):
        neighbor_set = self.graphlist[selected_node]
        current_community_set = self.node_map_to_community[selected_node]
        switch_community_set = set({})
        "Find communities to switch"
        "TODO:debug"
        "Find the community to switch in"
        inner_node_set =set({})
        for community in current_community_set:
            inner_node_set.update(neighbor_set.intersection(self.community_map_to_node[community]))
        external_node_set = neighbor_set - inner_node_set
        community_number_dict = defaultdict(lambda: 0)
        for node_e in external_node_set:
            for community_e in self.node_map_to_community[node_e]:
                community_number_dict[community_e] += 1
        if len(community_number_dict) == 0:
            return -100,-200,{},-100
        e_max = max(community_number_dict.itervalues())
        if e_max < len(inner_node_set):
            return -100,-100,{},-100
        "print community_number_dict"
        if e_max == 1:
            switch_community_set = self.node_map_to_community[min(external_node_set, key=lambda x: len(self.graphlist[x]))]
        else:
            switch_community_set.update({community for (community,community_number) in community_number_dict.iteritems() if community_number == e_max})
        
        
        penalty = (len(current_community_set)-1)*self.overlapping_penalty
        
        max_community = None
        max_utility = -200
        
        utility_neighbors_dict = {}
        utility_neighbors_dict_final ={}
        utility_neighbors_now = self.utility_list[selected_node]
        for each_node in self.graphlist[selected_node]:
            utility_neighbors_now += self.utility_list[each_node]
            
        for each_community_out in current_community_set:
            for each_community_in in switch_community_set:
                
                self.node_map_to_community[selected_node].remove(each_community_out)
                self.community_map_to_node[each_community_out].remove(selected_node)
                
                self.node_map_to_community[selected_node].add(each_community_in)
                self.community_map_to_node[each_community_in].add(selected_node)
            
                utility_modularity = modularity.modified_modularity_node(self,selected_node)
                utility_permanence = permanence.permanence_node(self,selected_node)
                utility_switch = utility_modularity + utility_permanence - penalty
                
                "Calculate the utility for the neighbors"
                utility_neighbors_switch = utility_switch
                for each_node in self.graphlist[selected_node]:
                    utility_each_node = modularity.modified_modularity_node(self, each_node)\
                    + permanence.permanence_node(self, each_node)\
                    -(len(self.node_map_to_community[each_node])-1)*self.overlapping_penalty
                    utility_neighbors_switch += utility_each_node
                    utility_neighbors_dict[each_node] = utility_each_node
            
                self.node_map_to_community[selected_node].remove(each_community_in)
                self.community_map_to_node[each_community_in].remove(selected_node)
                
                self.node_map_to_community[selected_node].add(each_community_out)
                self.community_map_to_node[each_community_out].add(selected_node)
                """print utility_neighbors_switch,utility_neighbors_now
                print utility_switch"""
                "TODO:debug   when utility<0 node becomes greedy"
                if self.utility_list[selected_node]<0 and utility_switch>0 and utility_switch > max_utility:
                    max_utility = utility_switch
                    max_community = (each_community_out,each_community_in)
                    utility_neighbors_dict_final.update(utility_neighbors_dict)
                    utility_neighbors_now = utility_neighbors_switch
                    
                elif utility_neighbors_switch>=utility_neighbors_now:
                    max_utility = utility_switch
                    max_community = (each_community_out,each_community_in)
                    utility_neighbors_dict_final.update(utility_neighbors_dict)
                    utility_neighbors_now = utility_neighbors_switch
        if len(utility_neighbors_dict_final)==0:
            return -100,-100,{},-100
        return max_utility,max_community,utility_neighbors_dict_final,utility_neighbors_now
    
    
    def leave_a_community(self,selected_node):
        current_community_set = self.node_map_to_community[selected_node]
        if len(current_community_set) == 1:
            return -100,-300,{},-100
        penalty = (len(current_community_set)-1 -1)*self.overlapping_penalty
        max_community = -100
        max_utility = -300
        
        utility_neighbors_dict = {}
        utility_neighbors_dict_final ={}
        utility_neighbors_now = self.utility_list[selected_node]
        for each_node in self.graphlist[selected_node]:
            utility_neighbors_now += self.utility_list[each_node]
            
        for each_community in current_community_set:
            self.node_map_to_community[selected_node].remove(each_community)
            self.community_map_to_node[each_community].remove(selected_node)
            
            utility_modularity = modularity.modified_modularity_node(self,selected_node)
            utility_permanence = permanence.permanence_node(self,selected_node)
            utility_leave = utility_modularity + utility_permanence - penalty
            
            "Calculate the utility for the neighbors"
            utility_neighbors_leave = utility_leave
            for each_node in self.graphlist[selected_node]:
                utility_each_node = modularity.modified_modularity_node(self, each_node)\
                + permanence.permanence_node(self, each_node)\
                -(len(self.node_map_to_community[each_node])-1)*self.overlapping_penalty
                utility_neighbors_leave += utility_each_node
                utility_neighbors_dict[each_node] = utility_each_node
            
            self.node_map_to_community[selected_node].add(each_community)
            self.community_map_to_node[each_community].add(selected_node)
            if utility_neighbors_leave>utility_neighbors_now:
                utility_neighbors_now = utility_neighbors_leave
                max_utility = utility_leave
                max_community = each_community
                utility_neighbors_dict_final.update(utility_neighbors_dict)
        if len(utility_neighbors_dict_final)==0:
            return -100,-100,{-1,-1},-100
        return max_utility,max_community,utility_neighbors_dict_final,utility_neighbors_now

    

    
    
    
        
        
        
        
        
        
        
        
        
        