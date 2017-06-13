############################################################
# Module  : combine models
# Date    : April 24th, 2017
# Author  : Xiao Ling
############################################################

import os
import pickle 

from app           import *
from utilities     import *
from experiments.rank_all import *
from experiments.milp import *

############################################################
'''
	@Use: get subset of turk gold set with data. 
	@Input: - results_dir :: String, path to directory with results
			- gold_dir :: String, path to directory with golds
			- name :: String, name of gold standard 
'''
def mk_gold_has_ngram_data(results_dir, gold_dir, name):

	results_path = os.path.join(results_dir, name + '.pkl')
	out_path     = os.path.join(gold_dir, name + '-has-ngram-data.txt')

	if os.path.exists(results_path):

		print('\n\t>> filtering data set [' + name + '] for those cluters'
			  ' with ngram data')

		with open(results_path,'rb') as h:
			gold = pickle.load(h)

		has_data = []

		for _,rank in gold['ranking'].iteritems():
			probs = [ p for _,p in rank['raw'].iteritems() if p ]
			if probs:
				has_data.append(rank['gold'])


		write_gold(out_path, has_data)

		return out_path, has_data

	else:
		raise IOError("\n\t>> cannot find test set [" + name + "] at "
			          "directory:\n\t\t" + results_dir)


turk = golds['turk']
bcs  = golds['bcs']

_, turk_has_data = mk_gold_has_ngram_data(app.fetch('milp/results'), app.fetch('gold'), 'turk')
_, bcs_has_data  = mk_gold_has_ngram_data(app.fetch('milp/results'), app.fetch('gold'), 'bcs')





