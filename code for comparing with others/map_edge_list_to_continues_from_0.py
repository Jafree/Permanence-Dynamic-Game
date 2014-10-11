import os
def map_edge_to_continuous(source_file_path,target_file_path):
	scan_old_to_new = {}
	count = 0
	f= open(source_file_path)
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
	for line in f:
		if line.count("\t")>0:
			linepair = line.rstrip().split("\t")
		else:
			linepair = line.rstrip().split()
		w.write(str(scan_old_to_new[int(linepair[0])])+"\t"+str(scan_old_to_new[int(linepair[1])])+"\n")
	f.close()
	w.close()
direct = raw_input("Input the folder under which the files will be made to continuous\n")
if not os.path.exists(direct):
	print "Wrong" + direct
if not os.path.exists(direct + "/continuous/"):
	os.mkdir(direct + "/continuous/")
for filename in os.listdir(direct): 
	if os.path.isfile(direct + "/"+filename):
		
		map_edge_to_continuous(direct + "/"+filename,direct + "/continuous/"+filename)