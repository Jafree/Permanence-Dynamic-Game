from collections import defaultdict
import os
"""
This function is used for mapping the edge list to continuous from 0 and deleting the self loop
"""
def map_edge_to_continuous(source_file_path,target_file_path):
	scan_old_to_new = {}
	count = 0
	f = open(source_file_path)
	for line in f:
		if len(line)>1:
			if line.count("\t")>0:
				linepair = line.rstrip().split("\t")
			else:
				linepair = line.rstrip().split()
			if int(linepair[0]) not in scan_old_to_new:
				scan_old_to_new[int(linepair[0])] = count
				count += 1
			if int(linepair[1]) not in scan_old_to_new:
				scan_old_to_new[int(linepair[1])] = count
				count += 1
	f.close()
	f = open(source_file_path)
	w = open(target_file_path,"w")
	line_exist = defaultdict(set)
	for line in f:
		if line.count("\t")>0:
			linepair = line.rstrip().split("\t")
		else:
			linepair = line.rstrip().split()
		"If the linepair has exist, then don't copy"
		
		if linepair[0] in line_exist and linepair[1] in line_exist[linepair[0]]:
			continue
		if linepair[0] == linepair[1]:
			continue
		line_exist[linepair[0]].add(linepair[1])
		line_exist[linepair[1]].add(linepair[0])
		w.write(str(scan_old_to_new[int(linepair[0])])+"\t"+str(scan_old_to_new[int(linepair[1])])+"\n")
	f.close()
	w.close()
direct = raw_input("Input the folder under which the files will be made to continuous\n")
if not os.path.exists(direct):
	print "Wrong" + direct
if not os.path.exists(direct + "/unique_continuous/"):
	os.mkdir(direct + "/unique_continuous/")
for filename in os.listdir(direct): 
	if os.path.isfile(direct + "/"+filename):
		
		map_edge_to_continuous(direct + "/"+filename,direct + "/unique_continuous/"+filename)