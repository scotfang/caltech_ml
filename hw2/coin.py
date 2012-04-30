#!/usr/bin/env python
import random

def trial():
    c1 = None
    cmin = None
    head_freqs = []
    for i in range(1000):
        head_ct = 0
        for k in range(10):
            if random.randint(0, 1): 
                head_ct += 1
        v_freq = head_ct/10.0
        head_freqs.append(v_freq) 
        if i == 0:
            c1 = v_freq 
            cmin = v_freq
        if v_freq < cmin:
            cmin = v_freq
    rand_idx = random.randint(0, 999) 
    crand = head_freqs[rand_idx]
    #print c1, cmin, crand
    return (c1, cmin, crand)

if __name__ == "__main__": 
    all_trials = []
    for i in range(100000):
        c_vals = trial()
        all_trials.append(c_vals)
        if i%1000 == 0:
            print i/1000, "% done.."
    c1 = sum([ t[0] for t in all_trials ])/100000.0
    print "AVE c1", c1
    cmin = sum([ t[1] for t in all_trials ])/100000.0
    print "AVE cmin", cmin
    crand = sum([ t[2] for t in all_trials ])/100000.0
    print "AVE crand", crand
     
     

