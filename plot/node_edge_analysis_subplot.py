'''
Created on 2014/10/11

@author: free
'''
import matplotlib.pyplot as plt
import numpy as np
f1 = open("E:/9_Dataset/Evolving_Network/as-733/output_permanence_modularity_game/analysis_nodes_edges.txt")
node_numbers = []
edge_numbers = []
node_change_numbers = []
edge_change_numbers = []


for line in f1:
    if len(line)<=1:
        break
    linepair = line.rstrip().split()
    node_numbers.append(linepair[0])
    edge_numbers.append(linepair[1])
    node_change_numbers.append(linepair[2])
    edge_change_numbers.append(linepair[3])
node_change_numbers[0]=0
edge_change_numbers[0]=0
f1.close()

figure1=plt.subplot(221)  
figure2=plt.subplot(222)  
figure3=plt.subplot(223)  
figure4=plt.subplot(224)

x = np.arange(1,734,1)
plt.sca(figure1)
plt.ylabel("Node Numbers $n$")
plt.xlabel("Snapshots $t$")
plt.xlim(0,750)
plt.plot(x,node_numbers,color="blue")
plt.sca(figure2)

plt.ylabel("Edge Numbers $m$")
plt.xlabel("Snapshots $t$")
plt.xlim(0,750)
plt.plot(x,edge_numbers,color="red")

plt.sca(figure3)
plt.ylabel("Node Changes $nc$")
plt.xlabel("Snapshots $t$")
plt.xlim(0,750)
plt.semilogy(x,node_change_numbers,color="blue")

plt.sca(figure4)
plt.ylabel("Edge Changes $ec$")
plt.xlabel("Snapshots $t$")
plt.xlim(0,750)
plt.semilogy(x,edge_change_numbers,color="red")




plt.show()
