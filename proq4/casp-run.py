#!/usr/bin/env python

import argparse
import sys
import re
import os
import pandas as pd
import numpy as np
import proq4


parser = argparse.ArgumentParser(description = '''Run ProQ4 and format into CASP format''')
parser.add_argument('-msa', nargs=1, type= str, default=sys.stdin, help = 'Path to msa.')
parser.add_argument('-pdb', nargs='+', type= str, default=sys.stdin, help = 'Path to pdb.')
parser.add_argument('-out', nargs=1, type= str, default=sys.stdin, help = 'Path to outfie.')
#parser.add_argument('-id', nargs=1, type= str, default=sys.stdin, help = 'Path to pdb.')
#parser.add_argument('-target', nargs=1, type= str, default=none, help = 'Path to pdb.')
parser.add_argument('-author', nargs=1, type= str, default="XXXX-XXXX-XXXX-XXXX", help = 'Authorkey default XXXX-XXXX-XXXX-XXXX.')
#parser.add_argument('-out', nargs=1, type= str, default=sys.stdin, help = 'Path to outfile.')
args = parser.parse_args()


header="PFRMAT QA"
method="METHOD ProQ4\nMODEL 2\nQMODE 2"
remark="REMARK ProQ4"
# author="AUTHOR XXXX-XXXX-XXXX"
author="AUTHOR "+args.author[0]

def convert(x):
    d0=5
    score=d0*np.sqrt(1/x-1)
    if score < 15.0:
        return (score)
    else:
        return(15.0)
    
def convert_to_casp(pq4):
    count=0
    globscore=np.mean(pq4.lddt)
    f.write(str(round(globscore,3))+" ")
    for i in range(0,len(pq4.lddt)):
        f.write(str(round(pq4.lddt[i],3))+" ")
        count+=1
        if count>20:
            f.write("\n")
            count=0
    f.write("\nEND\n")

    

model = proq4.get_proq4()
name=re.sub(r'.*\/','',args.pdb[0])
ali=proq4.process_a3m(args.msa[0])
target=name[0:5]
out=args.out[0]
f = open(out, 'w')
f.write(header+"\n")
f.write("TARGET "+str(target)+"\n")
f.write(author+"\n"+remark+"\n"+method+"\n")
for pdb in args.pdb:
    id=re.sub(r'.*\/','',pdb)
    modelid=id[5:10]
    f.write(str(target)+str(modelid)+" ")
    #print ("TEST: ",model,ali,pdb)
    pred = proq4.predict(model, ali, pdb)
    convert_to_casp(pred)
f.close()
