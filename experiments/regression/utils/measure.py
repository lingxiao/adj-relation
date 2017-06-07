############################################################
# Module  : inference with elastic baseline
# Date    : April 24th, 2017
# Author  : Xiao Ling
############################################################

import os
import math
from utilities import *
from experiments.argmax import *
from experiments.rank_all import *
from experiments.regression import *

############################################################
'''
	Binomial models
'''
def Pr_s_le_t(G):

	def fn(s,t):

		s_ge_t = 0.0
		s_le_t = 0.0

		if t in G.out_neigh(s):
			s_le_t += sum(n for _,n in G.out_neigh(s)[t].iteritems())
			
		if t in G.in_neigh(s):
			s_ge_t += sum(n for _,n in G.in_neigh(s)[t].iteritems())

		# alpha_beta = max(1.0, s_ge_t + s_le_t)
		alpha_beta = 1.0

		return E_binomial( s_le_t
			             , s_ge_t + s_le_t
			             , alpha_beta
			             , alpha_beta
			             )

	return fn

'''
	@Use: given model and hack num tosses
	      find posterior probabilty of head
	      given model
'''
def Pr_s_le_t_model(model, phi):

	def fn(s,t):

		prob_vec = model.predict_proba(phi(s,t))[0]
		prob     = prob_vec[1]
		# h        = round(prob*1)
		return E_binomial(prob, 1, 1, 1)

	return fn

def Pr_s_le_t_combo(G, model, phi):

	real  = Pr_s_le_t(G)
	model = Pr_s_le_t_model(model,phi)

	def fn(s,t):
		prob = real(s,t)
		if prob == 0.5:
			return model(s,t)
		else:
			return prob

	return fn

'''
	@Use: Expected value of p for Bernoulli(p)
		  given h heads on n tosses
		  with prior parameter alpha and beta
'''
def E_binomial(h,n,alpha,beta):
	t   = n - h
	top = float(alpha + h)
	bot = float(alpha + beta + h + t)
	return top / bot

############################################################
'''
	Decision function using binomial prior
'''
def decide_fn_model_Binomial(model, phi):
	def fn(gold):
		return argmax_Omega(gold, Pr_s_le_t_model(model,phi))
	return fn

def decide_fn_both_binomial(G, model, phi):
	def fn(gold):
		return argmax_Omega(gold, Pr_s_le_t_combo(G,model,phi))
	return fn
