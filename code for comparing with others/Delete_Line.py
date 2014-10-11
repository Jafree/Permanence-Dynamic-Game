import os
direct = raw_input('Input the forder under which the files will be moved the first four lines:\n')
if not os.path.exists(direct):
    print "Wrong" + direct
for filename in os.listdir(direct): 
    if os.path.isfile(direct + "/"+filename):
        f=open(direct + "/"+filename)
        if not os.path.exists(direct +"/standard/"):
            os.mkdir(direct+"/standard/")
        w=open(direct +"/standard/"+filename,"w")
        for line in f:
            if line[0] != "#":
                w.write(line)
        f.close()
        w.close()