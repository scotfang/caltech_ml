#!/usr/bin/env python
from math import *

#Q5
def error(u, v):
    u = float(u) 
    v = float(v) 
    return (u*exp(v) - 2*v*exp(-u))**2
    
def u_prime(u, v):
    #Q5
    u = float(u) 
    v = float(v) 
    return 2*u*exp(2*v) + 4*u*v*exp(v-u) - 4*v*exp(v-u) - 8*v**2*exp(-2*u)
def v_prime(u, v):
    #Q5
    u = float(u) 
    v = float(v) 
    return 2*u**2*exp(2*v) - 4*u*v*exp(v-u) - 4*u*exp(v-u) + 8*v*exp(-2*u)

def gd_step(lr, u, v, u_partial, v_partial):
    #lr - learning rate
    diff_u = lr*u_partial(u,v)  
    diff_v = lr*v_partial(u,v)  
    print "%f %f Stepping magnitude %f" % (u, v, sqrt(diff_u**2+diff_v**2))
    u -= diff_u
    v -= diff_v 
    print "new err", error(u,v)
    return (u, v)

def gd_iterate(u_start=1, v_start=1, lr=0.1, term_err=10e-14):
    #default params are for Q5
    u = u_start
    v = v_start
    its = 0
    while(error(u, v) > term_err):
        u, v = gd_step(lr, u, v, u_prime, v_prime); 
        its += 1
    print "GD Terminated with err %f on iteration %d" % (term_err, its)

def cd_step(lr, u, v):
    #lr - learning rate
    diff_u = lr*u_prime(u,v)  
    u -= diff_u
    diff_v = lr*v_prime(u,v)  
    v -= diff_v 
    print "%f %f Stepped u:%f v:%f" % (u, v, diff_u, diff_v)
    print "new err", error(u,v)
    return (u, v)

def coord_gd_iterate(u_start=1, v_start=1, lr=0.1, do_its=15):
    #Q7 "coordinate descent" 
    u = u_start
    v = v_start
    its = 0
    while(its<do_its):
        u, v = cd_step(lr, u, v); 
        its += 1
    print "Coordinate GD Terminated with err", error(u,v), "after %d iterations" % (its)

   
if __name__ == "__main__": 
    #gd_iterate(lr=0.1);
    coord_gd_iterate(lr=0.1);
