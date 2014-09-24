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
                self.graphlist[linepair[0]].add(linepair[1])
                self.graphlist[linepair[1]].add(linepair[0])
        "Store the node count and edge count"
        self.node_count = len(self.graphlist)
        self.edge_count = sum(len(i) for i in self.graphlist.itervalues())/2
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
    
    def permanence_modularity_community(self,last_graph=None,initial="restart",select="random",penalty=10):
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
        if initial == "restart" or (last_graph == None):
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
            self.utility_list = {node : self.create_singleton_community(node)[0] for node in self.graphlist.iterkeys()}
            
        '''
        Each agent belongs to its community in last snapshot if it had exist in last snapshot;
        Otherwise, it will belong to its own singleton community.
        '''
        if initial == "resume":
            '''
            TODO:
            Realization
            '''
            """
            self.node_map_to_community = {node : last_graph.community_map_to_node[node] for node in last_graph.graphlist.iterkeys()}
            """
            pass
        
        
        if initial == "penalty":
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
            print len(disequilibrium_node_list)
            "Random strategy"
            if select == "random":
                "Control the loop number"
                loop_count += 1
                if loop_count >= 10 * self.node_count:
                    break
                selected_node = random.choice(disequilibrium_node_list.keys())
                del disequilibrium_node_list[selected_node]
            
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
            utility_singleton,singleton_community = self.create_singleton_community(selected_node)
            "Join a new community,join_community = community to be joined"
            utility_join,join_community = self.join_a_community(selected_node)
            "Switch a community,switch_community =(community to be switched out, community to be in)"
            utility_switch,switch_community = self.switch_a_community(selected_node)
            "Leave a community,leave_community = community to be leaved"
            utility_leave,leave_community = self.leave_a_community(selected_node)
            utility_max = max(utility_singleton, utility_join, utility_switch, utility_leave)
            
            "If the utility doesn't increase, continue "
            if utility_max <= self.utility_list[selected_node]:
                continue
            "Otherwise, update the utility value for selected_node"
            self.utility_list[selected_node] = utility_max
            "To each scenario, we update the node to community and community to node dictionaries"
            if abs(utility_max - utility_switch)<0.0001:
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
            elif abs(utility_max - utility_join)<0.0001:
                self.node_map_to_community[selected_node].add(join_community)
                self.community_map_to_node[join_community].add(selected_node)
                """Add selected node's neighbors which is in join in community in the disequilibrium_list"""
                for each_node in self.graphlist[selected_node]:
                    if join_community not in self.node_map_to_community[each_node]:
                        disequilibrium_node_list[each_node] = len(self.graphlist[each_node])
            elif abs(utility_max - utility_leave)<0.0001:
                self.node_map_to_community[selected_node].remove(leave_community)
                self.community_map_to_node[leave_community].remove(selected_node)
                if len(self.community_map_to_node[leave_community])==0:
                    del self.community_map_to_node[leave_community]
                """Add selected node's neighbors which is in leave community in the disequilibrium_list"""
                for each_node in self.graphlist[selected_node]:
                    if leave_community in self.node_map_to_community[each_node]:
                        disequilibrium_node_list[each_node] = len(self.graphlist[each_node])
            elif abs(utility_max - utility_singleton)<0.0001:
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
            "Update the utility for each node in the neighbor set"
            for each_node in self.graphlist[selected_node]:
                self.utility_list[each_node] = \
                permanence.permanence_node(self, each_node)+\
                modularity.modified_modularity_node(self, each_node)-\
                (len(self.node_map_to_community[each_node])-1)*self.overlapping_penalty
                "disequilibrium_node_list[each_node] = len(self.graphlist[each_node])"
                
        return True
    
    
    
    def create_singleton_community(self,selected_node):
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
        
    def join_a_community(self,selected_node):
        
        current_community_set = self.node_map_to_community[selected_node]
        penalty = (len(current_community_set)+1 -1)*self.overlapping_penalty
        join_community_set = set({})
        "Find communities to join"
        for each_node in self.graphlist[selected_node]:
            for each_community in self.node_map_to_community[each_node]:
                if each_community not in current_community_set:
                    join_community_set.add(each_community)
        "When the selected_node and its neighbors are in the same community"
        if len(join_community_set)==0:
            return -100,-100
        "Calculate the utility of each community to join in "
        max_community = -100
        max_utility = -100
        for a_community in join_community_set:
            self.node_map_to_community[selected_node].add(a_community)
            self.community_map_to_node[a_community].add(selected_node)
            
            utility_modularity = modularity.modified_modularity_node(self,selected_node)
            utility_permanence = permanence.permanence_node(self,selected_node)
            utility_join = utility_modularity + utility_permanence - penalty
            
            self.node_map_to_community[selected_node].remove(a_community)
            self.community_map_to_node[a_community].remove(selected_node)
            if utility_join > max_utility:
                max_utility = utility_join
                max_community = a_community
        return max_utility,max_community
    
    def switch_a_community(self,selected_node):
        current_community_set = self.node_map_to_community[selected_node]
        switch_community_set = set({})
        "Find communities to switch"
        for each_node in self.graphlist[selected_node]:
            for each_community in self.node_map_to_community[each_node]:
                if each_community not in current_community_set:
                    switch_community_set.add(each_community)
        if len(switch_community_set) == 0:
            return -100,-200
        
        penalty = (len(current_community_set)-1)*self.overlapping_penalty
        
        max_community = None
        max_utility = -200
        for each_community_out in current_community_set:
            for each_community_in in switch_community_set:
                
                self.node_map_to_community[selected_node].remove(each_community_out)
                self.community_map_to_node[each_community_out].remove(selected_node)
                
                self.node_map_to_community[selected_node].add(each_community_in)
                self.community_map_to_node[each_community_in].add(selected_node)
            
                utility_modularity = modularity.modified_modularity_node(self,selected_node)
                utility_permanence = permanence.permanence_node(self,selected_node)
                utility_switch = utility_modularity + utility_permanence - penalty
            
                self.node_map_to_community[selected_node].remove(each_community_in)
                self.community_map_to_node[each_community_in].remove(selected_node)
                
                self.node_map_to_community[selected_node].add(each_community_out)
                self.community_map_to_node[each_community_out].add(selected_node)
                if utility_switch > max_utility:
                    max_utility = utility_switch
                    max_community = (each_community_out,each_community_in)
        return max_utility,max_community
    
    
    def leave_a_community(self,selected_node):
        current_community_set = self.node_map_to_community[selected_node]
        if len(current_community_set) == 1:
            return -100,-300
        penalty = (len(current_community_set)-1 -1)*self.overlapping_penalty
        max_community = -100
        max_utility = -300
        for each_community in current_community_set:
            self.node_map_to_community[selected_node].remove(each_community)
            self.community_map_to_node[each_community].remove(selected_node)
            
            utility_modularity = modularity.modified_modularity_node(self,selected_node)
            utility_permanence = permanence.permanence_node(self,selected_node)
            utility_leave = utility_modularity + utility_permanence - penalty
            
            self.node_map_to_community[selected_node].add(each_community)
            self.community_map_to_node[each_community].add(selected_node)
            if utility_leave > max_utility:
                max_utility = utility_leave
                max_community = each_community
        return max_utility,max_community

    

    
    
    
        
        
        
        
        
        
        
        
        
        