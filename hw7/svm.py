#!/usr/bin/env python

import sys
sys.path.append("..")
from utils import *
import random
import cvxopt
from cvxopt import solvers
from math import fabs
           
def gen_sample_and_linear_separator(N):
    sample = gen_sample(N)
    target_ok = 0
    target_fn = None

    while target_ok == 0: 
        target_fn = Linear_Fn()     
        sign = target_fn.eval(sample[0])
        for point in sample[1:]:
            if sign != target_fn.eval(point):
                target_ok = 1
                break
    return sample, target_fn       

class PLA_Fn(object):
    def __init__(self, sample, target_fn):
        self.weights = [0] * (len(sample[0])+1) 
        self.target_fn = target_fn
        self.sample = sample 
        self.converged = 0
        self.its = 0;

    def eval(self, x):
        return eval_lr_fn(self.weights, [1]+x)

    def learn(self):
        misclassified = filter(lambda p: self.target_fn.eval(p) != self.eval(p), self.sample)
        if len(misclassified) == 0:
            self.converged = 1
            return 

        self.its += 1
        critical_point = random.choice(misclassified)
        true_sign = self.target_fn.eval(critical_point)

        aug_cp = [1] + critical_point 
        assert(len(aug_cp) == len(self.weights))
        for i in range(len(self.weights)):
            self.weights[i] += aug_cp[i]*true_sign

    def plot(self):
        plot_linreg(self.target_fn, self.sample, self.weights)

    def get_eout(self, out_sample):
        n_err = len(filter(lambda p: self.target_fn.eval(p) != self.eval(p), out_sample))
        return n_err*1.0/len(out_sample)

class SVM_Fn(object):
    def __init__(self, sample, target_fn):
        self.dim = len(sample[0]) 
        self.sample = sample
        self.target_fn = target_fn
        
        P = cvxopt.spmatrix(1, range(self.dim+1), range(self.dim+1), tc='d')
        print "P", P
        q = cvxopt.matrix([0]*(self.dim+1), tc='d')

        aug_sample = []
        for point in sample:
            y = target_fn.eval(point)
            assert(y == 1 or y == -1)
            aug_point = [1] + point
            assert(len(aug_point) == self.dim +1)
            aug_point = [x*-1.0*y for x in aug_point]
            aug_sample.append(aug_point) 
           
        G = cvxopt.matrix(aug_sample, tc='d')
        G = G.trans() #not sure if this tranpose is safe
        h = cvxopt.matrix([-1]*len(sample), tc='d')
        
        self.qp_sln = cvxopt.solvers.qp(P, q, G, h)
        assert(self.qp_sln['status'] == 'optimal')
        self.weights = list(self.qp_sln['x'])
        self.in_err = filter(lambda p: self.target_fn.eval(p) != self.eval(p), self.sample)

        self.support_vectors = filter(lambda p: fabs(1-target_fn.eval(p)*dot_prod(self.weights, [1]+p)) < 0.001, sample) 

    def eval(self, x):
        return eval_lr_fn(self.weights, [1]+x)

    def plot(self):
        plot_linreg(self.target_fn, self.sample, self.weights)

    def get_eout(self, out_sample):
        n_err = len(filter(lambda p: self.target_fn.eval(p) != self.eval(p), out_sample))
        return n_err*1.0/len(out_sample)
    
def svm_vs_pla(N):
    while True:
        sample, target_fn = gen_sample_and_linear_separator(N);
        try:
            svm = SVM_Fn(sample, target_fn)
        except AssertionError:
            continue
        break;
    #svm.plot()

    perceptron = PLA_Fn(sample, target_fn)
    while not perceptron.converged:
        perceptron.learn()
    #perceptron.plot()

    out_sample = gen_sample(10000)
    print "Eout: svm %f pla %f" % (svm.get_eout(out_sample), perceptron.get_eout(out_sample))
    print "support vectors", svm.support_vectors

    if (svm.get_eout(out_sample) < perceptron.get_eout(out_sample)):   
        return True, len(svm.support_vectors)
    return False, len(svm.support_vectors)
    
def do_q8():
    N = 10
    results = [svm_vs_pla(N) for i in range(1000)]
    print "svm beat pla %f percent of the time" % len(filter(lambda r: r[0] is True, results))*1.0/N
              
def do_q9_q10():
    N = 100 
    results = [svm_vs_pla(N) for i in range(1000)]
    print "results", results
    
    percent_svm_won = len([r[0] for r in results if r[0] is True])*1.0/len(results)
    print "question 9: svm beat pla %f percent of the time" % percent_svm_won 

    ave_support_vectors = sum([r[1] for r in results])*1.0/len(results) 
    print "question 10: average support vectors", ave_support_vectors 
    
if __name__ == "__main__":
    do_q9_q10()

