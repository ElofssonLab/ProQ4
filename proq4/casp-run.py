#!/usr/bin/env python

import argparse
import sys
import os
import pandas as pd
import numpy as np
import proq4


parser = argparse.ArgumentParser(description = '''format graph-QA for CASP''')
parser.add_argument('-msa', nargs=1, type= str, default=sys.stdin, help = 'Path to msa.')
parser.add_argument('-pdb', nargs=1, type= str, default=sys.stdin, help = 'Path to pdb.')
#parser.add_argument('-out', nargs=1, type= str, default=sys.stdin, help = 'Path to outfile.')
args = parser.parse_args()
localfile = args.loc[0]
globalfile = args.glob[0]


targets=globaldata['target_id'].drop_duplicates()
header="PFRMAT QA"
method="METHOD ProQ4\nMODEL 2\nQMODE 2"
remark="REMARK ProQ4"
author="AUTHOR 5229-7541-3942"

def convert(x):
    d0=5
    score=d0*np.sqrt(1/x-1)
    if score < 15.0:
        return (score)
    else:
        return(15.0)
    
def convert_to_casp(pq4):
    tempglob=globaldata.loc[globaldata['target_id']==target]
    temploc=localdata.loc[localdata['target_id']==target]
    models=tempglob['decoy_id'].drop_duplicates()
    f = open(outdir+"/"+target+".QA", 'w')
    f.write(header+"\n")
    f.write("TARGET "+str(target)+"\n")
    f.write(author+"\n"+remark+"\n"+method+"\n")
    count=0
    for model in models:
        globscore=tempglob.loc[tempglob['decoy_id']==model]['gdtts'].max()
        temp=temploc.loc[temploc['decoy_id']==model]['lddt']
        locscore=temp.apply(lambda x:convert(x)).to_list()
        f.write(str(target)+str(model)+" ")
        f.write(str(round(globscore,3))+" ")
        
        for i in range(0,len(locscore)):
            f.write(str(round(locscore[i],3))+" ")
            count+=1
            if count>20:
                f.write("\n")
                count=0
        f.write("\nEND\n")
    f.close()
    

model = proq4.get_proq4()
ali=arg.msa[0]
for pdb in arg.pdb:
    pred = proq4.predict(model, ali, pdb)
    convert_to_casp(pred)
    
