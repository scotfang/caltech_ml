#!/usr/bin/env python

import sys
sys.path.append("..")
from utils import *

def get_validation_data(file, n_train, n_val):
    vals = parse_datfile(file);
    assert(n_train + n_val == len(vals))
    d_train = vals[0:n_train]
    d_val = vals[n_train:]
    return d_train, d_val

def transform( inputs, k ):
    assert(len(inputs[0])==2)
    t_data = []
    for x, y in inputs:
        t_input = [ 1, x, y, x**2, y**2, x*y, fabs(x-y), fabs(x+y) ]
        t_input = t_input[:k+1]
        assert(len(t_input) == k+1)
        t_data.append(t_input) 
    return t_data

class LR_Result(object):
    def __init__(self, w, ein=0, eout=0, actual_eout=None):
        self.w=w
        self.ein=ein
        self.eout=eout
        self.actual_eout = actual_eout 
    def __repr__(self):
        s = str(len(self.w)-1) + " ein:%f eout:%f" % (self.ein, self.eout)
        if self.actual_eout != None:
            s += " actual_eout:%f" % (self.actual_eout)
        return s

def validate_lr_kparams(in_dataf, out_dataf, n_train, n_val):
    print "validating k_params for n_train:%d n_val:%d" % (n_train, n_val)
    d_train, d_val = get_validation_data(in_dataf, n_train, n_val)
    train_inputs = [ [x,y] for x,y,z in d_train]
    train_outputs = [ z for x,y,z in d_train]
    val_inputs = [ [x,y] for x,y,z in d_val]
    val_outputs = [ z for x,y,z in d_val]
    k_range = [2,3,4,5,6,7] 
    res_key = {}
    
    min_result = None
    for k in k_range:
        t_data = transform(train_inputs, k) 
        w = linear_reg(t_data, train_outputs)
        ein = lr_get_error_pct(w, t_data, train_outputs)
        v_data = transform(val_inputs, k)
        eout = lr_get_error_pct(w, v_data, val_outputs)
        res_key[k] = LR_Result(w, ein, eout)
        print res_key[k]
        if min_result is None or eout < min_result.eout:
            min_result = res_key[k]
    print "Min ~Eout after training/validation", min_result 

    out_d = parse_datfile(out_dataf)
    out_inputs = [ [x,y] for x,y,z in out_d]
    out_outputs = [ z for x,y,z in out_d]
   
    min_eout_result = None
    print "Processing real eouts" 
    for k in k_range:
        t_data = transform(out_inputs, k)
        res_key[k].actual_eout = lr_get_error_pct(res_key[k].w, t_data, out_outputs)
        if min_eout_result is None or res_key[k].actual_eout < min_eout_result.actual_eout:
            min_eout_result = res_key[k]
        print res_key[k]
    print "Min Actual Eout", min_eout_result

def cross_validation_q7(a):
    #a == alpha
    a = float(a)
    #return (1+a)**2*(a-1)**2 + 4*((1+a)**2+(a-1)**2)
    return 1 + 4/(1+a)**2 + 4/(a-1)**2 
             
if __name__ == "__main__":
    #validate_lr_kparams("in.dta", "out.dta", 25, 10)
    #validate_lr_kparams("in.dta", "out.dta", 10, 25)
    alphas = [ sqrt(sqrt(3)-1), sqrt(9-sqrt(66)), sqrt(9+4*sqrt(6)), 10**30 ]
    for a in alphas:
        print cross_validation_q7(a)

