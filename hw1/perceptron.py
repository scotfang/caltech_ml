#!/usr/bin/env python
import random
from numpy import *
import Gnuplot, Gnuplot.funcutils
import itertools

def gen_sample(sample_size):
    sample = [] 
    x_vec = [-1, 1]
    y_vec = [-1, 1]
    for i in range(sample_size):
        sample.append([random.uniform(-1, 1), random.uniform(-1, 1)]);
    #print "Generated sample", sample
    return sample

def gen_target_fn():
    points = gen_sample(2)
    slope = (points[1][1]-points[0][1])/(points[1][0]-points[0][0])
    constant = points[1][1] - points[1][0]*slope
    print "slope", slope, "constant", constant
    check_constant = points[0][1] - points[0][0]*slope
    #print "check_constant", check_constant
    return slope, constant

def eval_target_fn(slope, constant, points):
    if points[1] - slope*points[0] - constant < 0:
        return -1
    return 1

def eval_hyp_fn(weights, points):
    if points[0]*weights[0] + points[1]*weights[1] + weights[2] < 0:
        return -1
    return 1

def plot(slope, constant, points, weights):
    g = Gnuplot.Gnuplot(debug=1)
    #g('set data style linespoints') # give gnuplot an arbitrary command
    # Plot a list of (x, y) pairs (tuples or a numpy array would
    # also be OK):
    #x1 = arange(10, dtype='float_')
    x1 = array([ (-1+x*0.1) for x in range(20) ])
    y1 = x1*slope + constant
    d1 = Gnuplot.Data(x1, y1, with_="lines")
    #g.plot(Gnuplot.Func("y = %fx + %f" % (slope, constant), title='target_func'), d1)

    #x2 = arange(10, dtype='float_')
    x2 = array([ (-1+x*0.1) for x in range(20) ])
    y2 = (-1/weights[1])*(weights[0]*x2+weights[2]) 
    d2 = Gnuplot.Data(x2, y2, with_="lines")
    #g.plot(Gnuplot.Func("y = %fx + %f" % (slope, constant), title='hypothesis'), d2)
    g('set data style linespoints') # give gnuplot an arbitrary command
    g.plot(points, d1, d2)
    raw_input('Please press return to continue...\n')

def get_badprob(slope, constant, weights):
    incs = [ -1 + .002*i for i in range(1001) ]
    big_set = itertools.product(incs, incs)
    bad_count = 0.0
    tot_ct = 0
    for pt in big_set:
        true_sign = eval_target_fn(slope, constant, pt)
        actual_sign = eval_hyp_fn(weights, pt)
        if true_sign != actual_sign:
            bad_count += 1
        tot_ct +=1
    print "bad count", bad_count
    return bad_count/(1001*1001)

def main():
    sample_sizes = (10, 100)
    for sample_size in sample_sizes: 
        converges = []
        bad_probs = []
        for i in range(1000):
            slope, constant = gen_target_fn() 
            sample = gen_sample(sample_size)
            it = 0
            weights = [0, 0, 0]
            while(1):
                bad_points = []
                for points in sample:
                    true_sign =     eval_target_fn(slope, constant, points)
                    actual_sign =   eval_hyp_fn(weights, points)  
                    if not len(bad_points) and true_sign != actual_sign:
                        bad_points.append(points)
                        weights[0] += points[0]*true_sign 
                        weights[1] += points[1]*true_sign 
                        weights[2] += true_sign 
                if not bad_points:
                    break
                #print "bad point", bad_points[0]
                it += 1
                if it%10 == 0:
                    #print "it", it, "bad_points", len(bad_points)
                    pass

            #print "weights", weights    
            print "converged on iteration", it
            converges.append(it)
            
            bad_prob = get_badprob(slope, constant, weights)
            print "bad_prob", bad_prob 
            bad_probs.append(bad_prob)
            #plot(slope, constant, sample, weights)
        print "FINISHED sample_size", sample_size
        print "avg convergence", sum(converges)/1000.0
        print "avg bad_prob", sum(bad_probs)/1000.0
    print "EXITING"

if __name__ == "__main__":
    main()
