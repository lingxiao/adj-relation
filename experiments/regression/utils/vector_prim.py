############################################################
# Module  : vector primitives
# Date    : April 24th, 2017
# Author  : Xiao Ling
############################################################

import math
import numpy as np
from utilities import *

############################################################
'''
	@Use: given set of pairs and feature representation function
		  rho of each word, and a function that combines
		  the pair of words, output the X matrix
	@Input:  - xs  :: [(String,String)]	  
			 - rho :: String -> numpy.array
			 - op  :: numpy.array -> numpy.array -> numpy.array

	@Output: - X :: numpy.array 
				dim : n x m   where n is the number of examples
							  and m is number of features
'''
def to_X(xs, rho, op):
	X = np.array([ op(rho(s),rho(t)) for s,t in xs ])
	return X

def to_x(rho,op):
	def fn(s,t):
		return op(rho(s),rho(t)).reshape(1,-1)
	return fn

############################################################
'''
	combine two rhos
'''
def vec_subtract(rho1, rho2):
	return rho1 - rho2

def vec_concat(rho1, rho2):
	return np.concatenate((rho1,rho2), axis = 0)

def vec_add(rho1, rho2):
	return rho1 + rho2



