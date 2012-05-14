#!/usr/bin/env python

import sys
sys.path.append("..")
from utils import *

def parse_datfile(file):
    vals = []
    f = open(file, "rb") 
    for line in f:
        vals.append( [ float(s) for s in line.split() ] )
    f.close()
    return vals

def transform( inputs ):
    assert(len(inputs[0])==2)
    t_data = []
    for x, y in inputs:
        t_input = [ 1, x, y, x**2, y**2, x*y, fabs(x-y), fabs(x+y) ]
        t_data.append(t_input) 
    return t_data

def do_weight_decay(reg_lambda):
    reg_lambda = float(reg_lambda)
    in_data = parse_datfile("in.dta") 
    inputs = [ [x,y] for x,y,z in in_data ]
    t_inputs = transform(inputs)
    outputs = [z for x,y,z in in_data]  
    w = lr_weight_decay(t_inputs, outputs, reg_lambda)
    
    in_sample_misclassified = 0
    for idx, input in enumerate(t_inputs):
        if eval_lr_fn(w, input) != outputs[idx]:
            in_sample_misclassified += 1

    out_data = parse_datfile("out.dta")
    inputs = [ [x,y] for x,y,z in out_data ]
    t_inputs = transform(inputs)
    outputs = [z for x,y,z in out_data]  

    out_sample_misclassified = 0
    for idx, input in enumerate(t_inputs):
        if eval_lr_fn(w, input) != outputs[idx]:
            out_sample_misclassified += 1
  
    out_sample_err = out_sample_misclassified*1.0/len(out_data)
    print "regularization lambda", reg_lambda, "in-sample err:", in_sample_misclassified*1.0/len(in_data), "out-sample err:", out_sample_err
    return out_sample_err 

def do_q6():
    do_weight_decay(10**2) 
    do_weight_decay(10**1) 
    do_weight_decay(10**0) 
    do_weight_decay(10**-1) 
    do_weight_decay(10**-2) 

def do_q7():
    min_err = None #(k, out_sample_err)
    k_range = range(-20, 20)
    k_range.reverse()
    for k in k_range:
        out_err = do_weight_decay(10**k)  
        if min_err is None or out_err < min_err[1]: 
            print "New min: k %d out_err %f" % (k, out_err)
            min_err = (k, out_err)

if __name__ == "__main__":
    do_weight_decay(10**3) 
