#!/usr/bin/env python
import sys
sys.path.append("..")
from utils import *
import gradient_descent
import random
from copy import copy

def logistic_fn(s):
    return exp(s) / (1+exp(s))

def cent_error(w, x, y):
    #cross-entropy error, y is +-1, the actual output in sample
    assert(len(w) == len(x))
    return log(1 + exp(-1*y*dot_prod(w, x))) 

def cent_partial_diffs(w, x, y):
    #generate all the partial derivatives of the cross-entropy error
    #given a weight vector (w), input vector (x), and binary +-1 output (y)
    assert(len(w) == len(x))
    partial_diffs = []
    for i in range(len(w)):
        diff = (-y*x[i]*exp(-y*dot_prod(w, x))) / (1 + exp(-y*dot_prod(w,x)))
        partial_diffs.append(diff)
    #print "partial_diffs", partial_diffs
    return partial_diffs

def sgd_step(lr, w, partial_diffs):
    #lr - learning rate
    assert(len(w) == len(partial_diffs))
    weighted_diffs = [lr*diff for diff in partial_diffs]
    step_norm = vec_mag(weighted_diffs)
    #print w,"stepped magnitude", step_norm
    for i in range(len(w)):
        w[i] -= weighted_diffs[i]  
    return step_norm

def plot_reg(target_fn, w, w_id, sample):
    #sample [(x,y)..]
    assert(len(w) == 3)

    g = Gnuplot.Gnuplot(debug=1)
    x = array([ (-1+x*0.1) for x in range(20) ])

    y_target = x*target_fn.slope + target_fn.constant
    d_target = Gnuplot.Data(x, y_target, with_="lines", title="target_func")

    y_reg = (-1/w[2])*(w[0]*1+w[1]*x) 
    d_reg = Gnuplot.Data(x, y_reg, with_="lines", title=w_id)

    g('set data style linespoints')
    g.plot(sample, d_target, d_reg)
    raw_input('Please press return to continue...\n')

def sgd_logreg(lr=0.1, N=100, term_delta=0.005):
    #term_delta = minimum step magnituded during sgd
    sample = gen_sample(N)
    w = [0.0, 0.0, 0.0] 
    target_fn = Linear_Fn()
    epoch_delta = term_delta + 1 

    epochs = 0    
    input_order = range(N)
    while epoch_delta >= term_delta:       
        random.shuffle(input_order)
        old_w = copy(w)
        for i in input_order:
            x = [1] + sample[i]
            y = target_fn.eval(sample[i])
            partial_diffs = cent_partial_diffs(w, x, y)
            sgd_step(lr, w, partial_diffs)
        epochs += 1
        epoch_delta = vec_mag([ w[i]-old_w[i] for i in range(len(w))])      
        #print "w", w

    out_of_sample = gen_sample(N*10)
    bad_pts = [ p for p in out_of_sample if target_fn.eval(p) != eval_lr_fn(w, p)]
    e_out = 1.0*len(bad_pts)/len(out_of_sample)
    #plot_reg(target_fn, w, "#%dlogreg_delt%f_eout%f" % (epochs, epoch_delta, e_out), sample)
    print "logistic regression terminated after %d epochs with wdelta_norm %f, e_out%f" %(epochs, epoch_delta, e_out)
    return epochs, e_out 

if __name__ == "__main__":
    trials = 100 
    epochs = []
    e_outs = []
    lr = 0.1
    N = 100
    term_delta = 0.005
    for i in range(trials):
        ep, eo = sgd_logreg(lr, N, term_delta)
        epochs.append(ep)
        e_outs.append(eo)
    print "Average convergence epoch", ave(epochs)
    print "Average e_out", ave(e_outs)
    print "learning rate", lr, "N", N, "termination w_norm_delta", term_delta

