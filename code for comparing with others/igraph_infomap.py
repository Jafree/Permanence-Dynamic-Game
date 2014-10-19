'''
Created on 2014/10/2

@author: free
'''
import permanence_igraph
from igraph import Graph
import datetime
import os
direct = raw_input('Input the forder under which the files will be analyzed\n')
if not os.path.exists(direct):
    print "Wrong" + direct
if not os.path.exists(direct+"/output_others_code"):
    os.mkdir(direct+"/output_others_code")
time_cost = []
perm = []
modu = []
community_number = []
max_community_size = []
average_community_size = []
for filename in os.listdir(direct): 
    if os.path.isfile(direct + "/"+filename):
        print "Processing:"+direct + "/"+filename+"\n"
        start = datetime.datetime.now()
        g = Graph.Read_Edgelist(direct + "/"+filename, directed=False)
        "community = Graph.community_spinglass(g)"
        "dendrogram = Graph.community_fastgreedy(g)"
        "community = dendrogram.as_clustering()"
        "community = Graph.community_infomap(g)"
        community = Graph.community_label_propagation(g)
        "community = Graph.community_multilevel(g)"
        end = datetime.datetime.now()
        t = end - start
        time_cost.append(t.seconds)
        "TODO:perm"
        perm.append(permanence_igraph.permanence_igraph(g,community))
        modu.append(g.modularity(community))
        community_number.append(len(community))
        max_community = 0
        average_community = 0
        for i in xrange(len(community)):
            if len(community[i]) > max_community:
                max_community = len(community[i])
            average_community += len(community[i])
        average_community = average_community/float(len(community))
        max_community_size.append(max_community)
        average_community_size.append(average_community)
f = open(direct+"/output_others_code/analysis_label_propagation_oregon.txt","w")
for i in xrange(len(time_cost)):
    f.write(str(time_cost[i])+" "\
    +str(perm[i])+" "+str(modu[i])+\
    " "+str(community_number[i])+" "+str(max_community_size[i])+" "+str(average_community_size[i])+"\n")
f.close() 
print "Done!"
        