############################################################
# Module  : combine models
# Date    : April 24th, 2017
# Author  : Xiao Ling
############################################################

import os

from app           import *
from utilities     import *
from experiments.regression import *
from experiments.regression.utils import *

############################################################
'''
	model and feature space representation
'''
model_name = 'logistic-regression|ppdb-ngram|[nu^HT(s)`-`nu^HT(t)]|num_neigh=10|penalty=l1|C=0.4|num_tosses=1'
path       = os.path.join(work_dir['models'], model_name + '/model')

print('\n\t>> loading model from ' + model_name)
with open(path,'rb') as h:
	model = pickle.load(h)

data_set   = model_name.split('|')[1]
num_neigh  = int(model_name.split('|')[3].replace('num_neigh=',''))

fix, nu = 'HT' , nu_coin( graphs[data_set], num_neigh )
OP , op = '-'  , vec_subtract
phi     = to_x(nu,op)

decide = decide_fn_both_binomial(graphs['ppdb-ngram'], model, phi)
SAVE   = True

############################################################
'''
	run on all data set
'''
results_dir     = work_dir['results']
gold_root       = app.fetch('gold')
turk_ngram_data = os.path.join(gold_root, 'turk-has-ngram-data-2.txt')
bcs_ngram_data  = os.path.join(gold_root, 'bcs-has-ngram-data-2.txt' )

turk = read_gold(turk_ngram_data)
bcs  = read_gold(bcs_ngram_data)

print('\n\t>> ranking turk cluster with ngram data in milp ...')
rank_all_gold( turk
	         , decide
	         , os.path.join(results_dir, 'turk-has-ngram-data.txt')
	         , save = SAVE )

print('\n\t>> ranking bcs cluster with ngram data in milp ...')
rank_all_gold( bcs
	         , decide
	         , os.path.join(results_dir, 'bcs-has-ngram-data.txt')
	         , save = SAVE )


