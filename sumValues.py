import random as r
from ROOT import *

e=0.75
h=TH1F("h","",76,0,380)
for i in range(1000):
    count=0
    for i in range(1,380):
        if r.random()<0.75:
            count=count+1
    h.Fill(count)

h.Draw()
sys.exit()
f = open("output.txt", "r")
li=f.readlines()
su=0.
num=len(li)
count=0
r.seed(16)
for i in li:
    li_pre=i[:-2]
    #print li_pre
    su=float(li_pre)+su
    if r.random()<float(li_pre):
        count=count+1

print num
print su/num
print count
