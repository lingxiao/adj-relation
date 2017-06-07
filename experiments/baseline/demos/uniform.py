############################################################
# Module  : uniform baseline
# Date    : April 24th, 2017
# Author  : Xiao Ling
############################################################

from utilities     import *
from experiments.argmax import *
from experiments.rank_all import *
from experiments.baseline import *

############################################################
'''
	run baseline using uniform graph
'''
rint('\n\t>> ranking bcs with uniform graph baseline ...')
rank_all_gold( golds['bcs']
	         , decide_fn_uniform()
	         , os.path.join(work_dir['results'], 'uniform-bcs.txt')
	         , save = True)

print('\n\t>> ranking turk with uniform graph baseline ...')
rank_all_gold( golds['turk']
	         , decide_fn_uniform()
	         , os.path.join(work_dir['results'], 'uniform-turk.txt')
	         , save = True)

print('\n\t>> ranking moh with uniform graph baseline ...')
rank_all_gold( golds['mohit']
	         , decide_fn_uniform()
	         , os.path.join(work_dir['results'], 'uniform-moh.txt')
	         , save = True)

print('\n\t>> ranking mohit-no-ties with ngram graph ...')
rank_all_gold( golds['mohit-no-tie']
	         , decide_fn_uniform()
	         , os.path.join(work_dir['results'], 'uniform-moh-no-tie.txt')
	         , save    = True )

print('\n\t>> ranking turk-no-ties with ngram graph ...')
rank_all_gold( golds['turk-no-tie']
	         , decide_fn_uniform()
	         , os.path.join(work_dir['results'], 'uniform-turk-no-tie.txt')
	         , save    = True )

