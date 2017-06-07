############################################################
# Module  : pointwise estimation baseline using ppdb-ngram graph
# Date    : April 24th, 2017
# Author  : Xiao Ling
############################################################


from utilities     import *
from experiments.argmax import *
from experiments.rank_all import *
from experiments.baseline import *

############################################################
'''
	run baseline using ppdb-ngram graph
'''
G = graphs['ppdb-ngram']

print('\n\t>> ranking bcs with ppdb-ngram graph baseline ...')
rank_all_gold( golds['bcs']
	         , decide_fn(G)
	         , os.path.join(work_dir['results'], 'ppdb-ngram-bcs.txt')
	         , save = True)

print('\n\t>> ranking turk with ppdb-ngram graph baseline ...')
rank_all_gold( golds['turk']
	         , decide_fn(G)
	         , os.path.join(work_dir['results'], 'ppdb-ngram-turk.txt')
	         , save = True)

print('\n\t>> ranking mohit with ppdb-ngram graph baseline ...')
rank_all_gold( golds['mohit']
	         , decide_fn(G)
	         , os.path.join(work_dir['results'], 'ppdb-ngram-mohit.txt')
	         , save = True)


print('\n\t>> ranking mohit-no-ties with ppdb-ngram graph ...')
rank_all_gold( golds['mohit-no-tie']
	         , decide_fn(G)
	         , os.path.join(work_dir['results'], 'ppdb-ngram-mohit-no-tie.txt')
	         , save    = True )

print('\n\t>> ranking turk-no-ties with ppdb-ngram graph ...')
rank_all_gold( golds['turk-no-tie']
	         , decide_fn(G)
	         , os.path.join(work_dir['results'], 'ppdb-ngram-turk-no-tie.txt')
	         , save    = True )

