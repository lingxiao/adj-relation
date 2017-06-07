############################################################
# Module  : pointwise estimation baeline
# Date    : April 24th, 2017
# Author  : Xiao Ling
############################################################

from experiments.argmax import *
from utilities import *

############################################################
'''
	@Use: baseline Pr[ s < t ] using just pointwise esitmation
'''
def Pr_s_le_t(G):

	def fn(s,t):

		s_ge_t = 0.0
		s_le_t = 0.0

		if t in G.out_neigh(s):
			s_le_t += sum(n for _,n in G.out_neigh(s)[t].iteritems())
			
		if t in G.in_neigh(s):
			s_ge_t += sum(n for _,n in G.in_neigh(s)[t].iteritems())

		s_ge_t = max(1e-5,s_ge_t)	
		s_le_t = max(1e-5,s_le_t)	

		return s_le_t/(s_ge_t + s_le_t)

	return fn

############################################################
'''
	Decision Functions

	@Use: pick out algo from gold
'''
def decide_fn(G):
	def fn(gold):
		return argmax_Omega(gold, Pr_s_le_t(G))
	return fn

'''
	@Use: absolute baseline coin toss for each decision
'''
def decide_fn_uniform():

	def uniform_s_le_t(s,t):
		return 0.5

	def fn(gold):
		return argmax_Omega(gold, uniform_s_le_t)
	return fn
