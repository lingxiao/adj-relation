############################################################
# Module  : run winning model
# Date    : April 24th, 2017
# Author  : Xiao Ling
############################################################

from app           import *
from utilities     import *
from experiments.rank_all import *
from experiments.regression import *

############################################################
'''
	model and feature space representation
'''
winner = 'logistic-regression|ppdb-ngram|[nu^HT(s)`-`nu^HT(t)]|num_neigh=10|penalty=l1|C=0.4|num_tosses=1'
path   = os.path.join(work_dir['models'], winner + '/model')

print('\n\t>> loading model from ' + winner)
with open(path,'rb') as h:
	model = pickle.load(h)

data_set   = winner.split('|')[1]
num_neigh  = int(winner.split('|')[3].replace('num_neigh=',''))
G          = graphs[data_set]

fix, nu = 'HT' , nu_coin(G, num_neigh )
OP , op = '-'  , vec_subtract
phi     = to_x(nu,op)

decide = decide_fn_both_binomial(G, model, phi)
SAVE   = True

############################################################
'''
	run on all data set
'''
results_dir = os.path.join( work_dir['results'], winner)
						  
if not os.path.exists(results_dir):
	os.mkdir(results_dir)

readme = 'model:\t\t' + winner            + '\n' \
	   + 'inference data set:\t' + data_set + '\n' \

with open( os.path.join(results_dir,'readme.txt'), 'wb' ) as h:
	h.write(readme)

############################################################
'''
	run
'''
print('\n\t>> ranking dev with model ...')
rank_all_gold( golds['dev']
	         , decide
	         , os.path.join(results_dir, 'dev.txt')
	         , save = SAVE )

print('\n\t>> ranking bcs with model ...')
rank_all_gold( golds['bcs']
	         , decide
	         , os.path.join(results_dir, 'bcs.txt')
	         , save = SAVE )

print('\n\t>> ranking mohit with model ...')
rank_all_gold( golds['mohit']
	         , decide
	         , os.path.join(results_dir, 'mohit.txt')
	         , save = SAVE )

print('\n\t>> ranking mohit-no-ties model ...')
rank_all_gold( golds['mohit-no-tie']
	         , decide
	         , os.path.join(results_dir, 'mohit-no-tie.txt')
	         , save = SAVE )

print('\n\t>> ranking turk with model ...')
rank_all_gold( golds['turk']
	         , decide
	         , os.path.join(results_dir, 'turk.txt')
	         , save = SAVE )

print('\n\t>> ranking turk-no-ties model ...')
rank_all_gold( golds['turk-no-tie']
	         , decide
	         , os.path.join(results_dir, 'turk-no-tie.txt')
	         , save = SAVE )

