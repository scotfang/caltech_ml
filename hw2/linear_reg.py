#!/usr/bin/env python
import random
from numpy import *
from numpy import linalg as LA
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
    #print "target_fn: y= %dx + %d" % (slope, constant) 
    check_constant = points[0][1] - points[0][0]*slope
    #print "check_constant", check_constant
    return slope, constant

def eval_target_fn(slope, constant, points):
    val = points[1] - slope*points[0] - constant
    if val < 0:
        return -1
    return 1

def eval_lr_fn(weights, points):
    if weights[0] + points[0]*weights[1] + points[1]*weights[2] < 0:
        return -1
    return 1

def eval_percept_fn(weights, points):
    if points[0]*weights[0] + points[1]*weights[1] + weights[2] < 0:
        return -1
    return 1

def plot_linreg(slope, constant, points, weights):
    g = Gnuplot.Gnuplot(debug=1)
    x1 = array([ (-1+x*0.1) for x in range(20) ])
    y1 = x1*slope + constant
    print "y1", y1
    d1 = Gnuplot.Data(x1, y1, with_="lines", title="target_func")

    y2 = (-1/weights[-1])*(weights[0]+weights[1]*x1) 
    d2 = Gnuplot.Data(x1, y2, with_="lines", title="linreg_func")
    g('set data style linespoints') # give gnuplot an arbitrary command

    g.plot(points, d1, d2)
    raw_input('Please press return to continue...\n')

def plot_perceptron(slope, constant, points, weights):
    g = Gnuplot.Gnuplot(debug=1)
    x1 = array([ (-1+x*0.1) for x in range(20) ])
    y1 = x1*slope + constant
    d1 = Gnuplot.Data(x1, y1, with_="lines")

    x2 = array([ (-1+x*0.1) for x in range(20) ])
    y2 = (-1/weights[1])*(weights[0]*x2+weights[2]) 
    d2 = Gnuplot.Data(x2, y2, with_="lines")
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

def linear_reg(sample_inputs, target_vector):
    #print "target_vec", target_vector
    aug_inputs = [ [1,] + i for i in sample_inputs ]
    a = array(aug_inputs)
#    print "inputs", a, a.T
#    square = dot(a, a.T) 
#    print "square", square
#    inv_square = LA.inv(square) 
#    print "identity close", allclose(dot(square, inv_square), eye(square.shape[0]))
#    pseudo_inv = dot(inv_square, a).T
#    print "pseudo_inv", pseudo_inv
    pseudo_inv = LA.pinv(a)
    #print "pseudo_inv", pseudo_inv
    weights = dot(pseudo_inv , target_vector)
    #print "weights", weights
    return weights 

def main():
    sample_sizes = (10,)
    RUNS = 1000
    for sample_size in sample_sizes: 
        bad_probs = []
        converges = []
        for i in range(RUNS): #number of trials to run
            slope, constant = gen_target_fn() 
            sample_inputs = gen_sample(sample_size)
            target_vector = array([ (eval_target_fn(slope, constant, points), )
                                for points in sample_inputs ])
            weights = linear_reg(sample_inputs, target_vector) 
            bad_pts = 0
            for i, points in enumerate(sample_inputs):
                true_val = target_vector[i]
                lr_val = eval_lr_fn(weights, points)
                if true_val != lr_val:
                    bad_pts += 1
            bad_freq = 1.0*bad_pts/sample_size
            print "bad_freq", bad_freq
            #print "weights", weights    
            #plot_linreg(slope, constant, sample_inputs, weights)

            
            p_weights = [weights[1], weights[2], weights[0]]
            #p_weights = [0, 0, 0]
            #plot_perceptron(slope, constant, sample_inputs, p_weights)
            it = 0
            while(1):
                bad_points = []
                for i, points in enumerate(sample_inputs):
                    t_val = target_vector[i]
                    p_val = eval_percept_fn(p_weights, points)
                    if t_val != p_val:
                        bad_points.append([points, t_val])
                if not len(bad_points):
                    break;
                if len(bad_points) == 1: 
                    shift_pt = bad_points[0]
                else: 
                    shift_pt = bad_points[ random.randint(0, len(bad_points)-1)]
                #print "shift_pt", shift_pt
                #plot_perceptron(slope, constant, sample_inputs, p_weights)
                p_weights[0] += shift_pt[0][0]*shift_pt[1]
                p_weights[1] += shift_pt[0][1]*shift_pt[1]
                p_weights[2] += shift_pt[1]
                it += 1
                if(it % 100 == 0):
                    print "...PLA it", it
            print "PLA converged on iteration", it
            converges.append(it)
    print "Average PLA converged on iteration", sum(converges)*1.0/len(converges) 

if __name__ == "__main__":
    main()
