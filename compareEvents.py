#!/usr/bin/env python
import linecache

def Diff(li1, li2): 
    return (list(set(li1) - set(li2))) 


filename ="output-new.txt"
get = linecache.getline
list_new=[]
for i in range(1,80):
    line=get(filename,i)
    list_new.append(int(line.split(": ")[2].split("\n")[0]))

filename2 ="output_old.txt"
get2 = linecache.getline
list_old=[]
for i in range(1,77):
    line2=get2(filename2,i)
    #print line2.split(": ")[2].split("\n")[0]
    list_old.append(int(line2.split(": ")[2].split("\n")[0]))

x=set(list_new)
y=set(list_old)
print x.symmetric_difference(y)
#z=x.difference(y)
#print x&y
#print len(list_new)
#print len(list_old)
#print len(x)
#print len(y)
#print Diff(list_new,list_old)
#print z
list_new2=list_new
print list_new
print list_new2
i=0
for x in list_new:
    ii=0
    for y in list_new2:
        if x==y and i!=ii:
            print x
            #print i,ii
        ii=ii+1
    i=i+1
