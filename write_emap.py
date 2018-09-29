#!/usr/local/bin/python

import sys
from emap_tools import *

if __name__ == "__main__":


    if len(sys.argv) > 1:
        in_json_fname = sys.argv[1]
        print("## Input JSON emap file: " + in_json_fname)
    else:
        print("## No input JSON emap given!")
        exit(0)

    mdict = pd.read_json(in_json_fname, orient = 'records').T.to_dict()
    modules = [Module(**mdict[key]) for key in mdict]

    outfname = in_json_fname.replace('.json','.emap.txt')

    labels = ['CHIP' , 'CHANNEL' , 'layer','module_IX',  'module_IV' , 'IX',  'IV' , 'TYPE']
    with open(outfname,'w') as emapfile:
        for module in modules:
            emapfile.write(module.channels[labels].to_string(index=False) + '\n')

    print("## Emap file written: " + outfname)
