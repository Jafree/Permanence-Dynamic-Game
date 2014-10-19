'''
Created on 2014/10/11

@author: free
'''
import matplotlib.pyplot as plt
import numpy as np
import sys
sys.path.append("E:/9_Dataset/Evolving_network/as-733/output_permanence_modularity_game")
sys.path.append("E:/9_Dataset/Evolving_network/as-733/output_others_code")
f1 = open("E:/9_Dataset/Evolving_network/as-733/output_permanence_modularity_game/analysis.txt")
f2 = open("E:/9_Dataset/Evolving_network/as-733/output_others_code/analysis_infomap.txt")
f3 = open("E:/9_Dataset/Evolving_network/as-733/output_others_code/analysis_labelpropagation.txt")
f4 = open("E:/9_Dataset/Evolving_network/as-733/output_others_code/analysis_labelrankT.txt")
time_cost_1 = []
perm_1 = []
modu_1 = []
community_number_1 = []
max_community_size_1 = []
average_community_size_1 = []

time_cost_2 = []
perm_2 = []
modu_2 = []
community_number_2 = []
max_community_size_2 = []
average_community_size_2 = []

time_cost_3 = []
perm_3 = []
modu_3 = []
community_number_3 = []
max_community_size_3 = []
average_community_size_3 = []

time_cost_4 = []
perm_4 = []
modu_4 = []
community_number_4 = []
max_community_size_4 = []
average_community_size_4 = []
for line in f1:
    if len(line)<=1:
        break
    linepair = line.rstrip().split()
    time_cost_1.append(linepair[0])
    perm_1.append(linepair[1])
    modu_1.append(linepair[2])
    community_number_1.append(linepair[3])
    max_community_size_1.append(linepair[4])
    average_community_size_1.append(linepair[5])
for line in f2:
    if len(line)<=1:
        break
    linepair = line.rstrip().split()
    time_cost_2.append(linepair[0])
    perm_2.append(linepair[1])
    modu_2.append(linepair[2])
    community_number_2.append(linepair[3])
    max_community_size_2.append(linepair[4])
    average_community_size_2.append(linepair[5])
for line in f3:
    if len(line)<=1:
        break
    linepair = line.rstrip().split()
    time_cost_3.append(linepair[0])
    perm_3.append(linepair[1])
    modu_3.append(linepair[2])
    community_number_3.append(linepair[3])
    max_community_size_3.append(linepair[4])
    average_community_size_3.append(linepair[5])
for line in f4:
    if len(line)<=1:
        break
    linepair = line.rstrip().split()
    time_cost_4.append(linepair[0])
    perm_4.append(linepair[1])
    modu_4.append(linepair[2])
    community_number_4.append(linepair[3])
    max_community_size_4.append(linepair[4])
    average_community_size_4.append(linepair[5])
f1.close()
f2.close()
f3.close()
f4.close()
x = np.arange(1,734,1)
plt.ylabel("Modularity")
plt.xlabel("Snapshots")
plt.xlim(0,750)
plt.plot(x,max_community_size_1,color="blue",label="PDG")
plt.plot(x,max_community_size_2,color="red",label="Infomap")
#plt.plot(x,max_community_size_3,color="green",label="LabelPro")
#plt.plot(x,max_community_size_4,color="yellow",label="LabelRankT")



plt.legend(loc='upper left')
plt.show()
