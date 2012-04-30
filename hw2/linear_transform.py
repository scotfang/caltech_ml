#!/usr/bin/env python
import random
from numpy import *
from numpy import linalg as LA
import Gnuplot, Gnuplot.funcutils
import itertools
import math

class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

def gen_sample(sample_size):
    sample = [] 
    x_vec = [-1, 1]
    y_vec = [-1, 1]
    for i in range(sample_size):
        sample.append(Point(random.uniform(-1, 1), random.uniform(-1, 1)))
    return sample

def transform_sample(sample):
    ts = [[p.x, p.y, p.x*p.y, p.x**2, p.y**2] for p in sample]
    return ts

def gen_target_fn():
    points = gen_sample(2)
    slope = (points[1][1]-points[0][1])/(points[1][0]-points[0][0])
    constant = points[1][1] - points[1][0]*slope
    #print "target_fn: y= %dx + %d" % (slope, constant) 
    check_constant = points[0][1] - points[0][0]*slope
    #print "check_constant", check_constant
    return slope, constant

def eval_nonlinear_fn(point):
    if point.x**2 + point.y**2 - 0.6 > 0:
        return 1
    else:
        return -1

def eval_target_fn(slope, constant, points):
    val = points[1] - slope*points[0] - constant
    if val < 0:
        return -1
    return 1

def eval_lr_fn(weights, data_p):
    if weights[0] + p.x*weights[1] + p.y*weights[2] < 0:
        return -1
    return 1

def eval_transform_fn(weights, data_p):
    data_p = [1] + data_p 
    dp = 0
    for d, i in enumerate(data_p):
        dp += weights[i]*d
    if dp < 0:
        return -1
    return 1

def eval_percept_fn(weights, points):
    if points[0]*weights[0] + points[1]*weights[1] + weights[2] < 0:
        return -1
    return 1

def plot_linreg(points, weights):
    g = Gnuplot.Gnuplot(debug=1)
    x_cir = arange(16)*0.1+(-1*math.sqrt(0.6))
    y_cir = arange(21)*0.1 + -1
    xm = x_cir[:,newaxis]
    ym = y_cir[newaxis,:]
    m = x_cir**2 + y_cir**2 - 0.6
    g('set parametric')
    g('set data style lines')
    g('set hidden')
    g('set contour base')
    g.title('An example of a surface plot')
    g.xlabel('x')
    g.ylabel('y')
    # The `binary=1' option would cause communication with gnuplot to
    # be in binary format, which is considerably faster and uses less
    # disk space.  (This only works with the splot command due to
    # limitations of gnuplot.)  `binary=1' is the default, but here we
    # disable binary because older versions of gnuplot don't allow
    # binary data.  Change this to `binary=1' (or omit the binary
    # option) to get the advantage of binary format.
    g.splot(Gnuplot.GridData(m,x_cir,y_cir, binary=0))

        
#    x1 = array([ (-1+x*0.1) for x in range(20) ])
#    y2 = (-1/weights[-1])*(weights[0]+weights[1]*x1) 
#    d2 = Gnuplot.Data(x1, y2, with_="lines", title="linreg_func")
#    g('set data style linespoints') # give gnuplot an arbitrary command
#
#    g.plot(points, d1, d3, d2)
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
    aug_inputs = [ [1] + vec for vec in sample_inputs ]
    a = array(aug_inputs)
    print "linear_reg array", a
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
    sample_sizes = (5,)
    RUNS = 1 
    for sample_size in sample_sizes: 
        bad_probs = []
        for i in range(RUNS): #number of trials to run
            sample = gen_sample(sample_size)
            target_vector = array([ (eval_nonlinear_fn(p), ) 
                for p in sample])

            noisy_set = set([]) 
            while len(noisy_set) < len(target_vector)/10: 
                noisy_set.add(random.randint(0, len(target_vector)-1))
            #print "noisy set", noisy_set
            for n_idx in noisy_set:
                target_vector[n_idx] *= -1

            t_sample = transform_sample(sample)
            print "t_sample", t_sample
             
            weights = linear_reg(t_sample, target_vector) 
            print "weights", weights
            bad_pts = 0
            for i, p in enumerate(t_sample):
                true_val = target_vector[i]
                lr_val = eval_transform_fn(weights, p)
                if true_val != lr_val:
                    bad_pts += 1
            bad_freq = 1.0*bad_pts/sample_size
            print "bad_freq", bad_freq
            bad_probs.append(bad_freq)
            #print "weights", weights    
            #plot_linreg([(p.x, p.y) for p in sample], weights)
    print "AVE Ein", sum(bad_probs)*1.0/len(bad_probs)

if __name__ == "__main__":
    main()
