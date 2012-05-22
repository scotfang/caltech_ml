#!/usr/bin/env python

import sys
sys.path.append("..")
from utils import *
           
def gen_sample_and_linear_separator():
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
        self.weights = [0] * (sample[0]+1) 
        self.target_fn = target_fn
        self.sample = sample 
        self.converged = 0
        self.its = 0;

    def eval(self, points):
        aug_pts = [1] + points
        if dot_prod(aug_pts, weights) < 0:
            return -1
        return 1

    def learn(self):
        misclassified = filter(lambda p: self.target_fn.eval(p) != self.eval(p), self.sample)
        if !len(misclassified):
            self.converged = 1
            return 

        self.its += 1
        critical_point = random.choice(misclassified)
        true_sign = self.target_fn.eval(critical_point)

        aug_cp = [1] + critical_point 
        assert(len(aug_cp) == len(self.weights))
        for i in range(len(self.weights)):
            self.weights[i] += aug_cp[i]*true_sign

class SVM_Fn(object):
          
def svm_vs_pla():
    sample, target_fn = gen_sample_and_linear_separator();
    perceptron = PLA_Fn(sample, target_fn)
    
    
              
if __name__ == "__main__":

