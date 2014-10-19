'''
Created on 2014/10/13

@author: free
'''
import os
direct = raw_input('Input the forder under which the files will be moved the first four lines:\n')
if not os.path.exists(direct):
    print "Wrong" + direct
count = 1
if not os.path.exists(direct +"/as733_for_labelrankT/"):
    os.mkdir(direct+"/as733_for_labelrankT/")
for filename in os.listdir(direct): 
    if os.path.isfile(direct + "/"+filename):
        command = "copy " + direct +"\\"+filename + " " +direct +"\\as733_for_labelrankT\\"+str(count)+".txt"
        os.system(command)
        print command
        count += 1 
        
