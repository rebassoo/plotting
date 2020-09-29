#!/usr/bin/env python

def checkIfDuplicates_3(listOfElems):
    ''' Check if given list contains any duplicates '''    
    i=0
    for elem in listOfElems:
        if listOfElems.count(elem) > 1:
            i=i+1
            print elem
            #return True
    print i
    return False

fp=open('output_4.txt','r')
li=fp.readlines()

result = checkIfDuplicates_3(li)
if result:
    print('Yes, list contains duplicates')
else:
    print('No duplicates found in list')    
#long_string=fp.read()
#re_dict={}
