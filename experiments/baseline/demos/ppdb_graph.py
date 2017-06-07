############################################################
# Module  : pointwise estimation baseline using ppdb graph
# Date    : April 24th, 2017
# Author  : Xiao Ling
############################################################

from utilities     import *
from experiments.argmax import *
from experiments.rank_all import *
from experiments.baseline import *

############################################################
'''
	run baseline using ppdb graph
'''
G = graphs['ppdb']

print('\n\t>> ranking bcs with ppdb graph baseline ...')
rank_all_gold( golds['bcs']
	         , decide_fn(G)
	         , os.path.join(work_dir['results'], 'ppdb-bcs.txt')
	         , save = True)

print('\n\t>> ranking turk with ppdb graph baseline ...')
rank_all_gold( golds['turk']
	         , decide_fn(G)
	         , os.path.join(work_dir['results'], 'ppdb-turk.txt')
	         , save = True)

print('\n\t>> ranking moh with ppdb graph baseline ...')
rank_all_gold( golds['moh']
	         , decide_fn(G)
	         , os.path.join(work_dir['results'], 'ppdb-moh.txt')
	         , save = True)


print('\n\t>> ranking moh-no-ties with ngram graph ...')
rank_all_gold( golds['moh-no-tie']
	         , decide_fn(G)
	         , os.path.join(work_dir['results'], 'ppdb-moh-no-tie.txt')
	         , save    = True )

print('\n\t>> ranking turk-no-ties with ngram graph ...')
rank_all_gold( golds['turk-no-tie']
	         , decide_fn(G)
	         , os.path.join(work_dir['results'], 'ppdb-turk-no-tie.txt')
	         , save    = True )

