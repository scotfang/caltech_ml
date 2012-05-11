#!/usr/bin/env python
import random
from math import *
from numpy import *
from numpy import linalg as LA
import Gnuplot, Gnuplot.funcutils
import itertools
from operator import mul


def prod(x):
    return reduce(mul, x)

def ave(x):
    return 1.0*sum(x)/len(x)

def dot_prod(x, y):
    assert(len(x) == len(y))
    return sum([x[i]*y[i] for i in range(len(x))])

def vec_mag(x):
    return sqrt(sum([c**2 for c in x]))

def gen_sample(sample_size):
    sample = [] 
    x_vec = [-1, 1]
    y_vec = [-1, 1]
    for i in range(sample_size):
        sample.append([random.uniform(-1, 1), random.uniform(-1, 1)]);
    return sample

def eval_target_fn(slope, constant, point):
    val = point[1] - slope*point[0] - constant
    if val < 0:
        return -1
    return 1

def gen_target_fn():
    points = gen_sample(2)
    slope = (points[1][1]-points[0][1])/(points[1][0]-points[0][0])
    constant = points[1][1] - points[1][0]*slope
    #print "target_fn: y= %dx + %d" % (slope, constant) 
    #check_constant = points[0][1] - points[0][0]*slope
    #print "check_constant", check_constant
    return slope, constant

class Linear_Fn(object):
    def __init__(self):
        slope, constant = gen_target_fn()
        self.slope = slope
        self.constant = constant
    def eval(self, point):
        return eval_target_fn(self.slope, self.constant, point)

def eval_lr_fn(weights, point):
    assert(len(weights)==3 and len(point) == 2)
    if weights[0] + point[0]*weights[1] + point[1]*weights[2] < 0:
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
