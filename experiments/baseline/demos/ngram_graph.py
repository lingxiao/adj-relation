
############################################################
# Module  : pointwise estimation baseline using ngram graph
# Date    : April 24th, 2017
# Author  : Xiao Ling
############################################################


from utilities     import *
from experiments.argmax import *
from experiments.rank_all import *
from experiments.baseline import *

############################################################
'''
	run baseline using ngram graph
'''
G = graphs['ngram']

print('\n\t>> ranking bcs with ngram graph baseline ...')
rank_all_gold( golds['bcs']
	         , decide_fn(G)
	         , os.path.join(work_dir['results'], 'ngram-bcs.txt')
	         , save = True)

print('\n\t>> ranking turk with ngram graph baseline ...')
rank_all_gold( golds['turk']
	         , decide_fn(G)
	         , os.path.join(work_dir['results'], 'ngram-turk.txt')
	         , save = True)

print('\n\t>> ranking mohit with ngram graph baseline ...')
rank_all_gold( golds['mohit']
	         , decide_fn(G)
	         , os.path.join(work_dir['results'], 'ngram-mohit.txt')
	         , save = True)


print('\n\t>> ranking mohit-no-ties with ngram graph ...')
rank_all_gold( golds['mohit-no-tie']
	         , decide_fn(G)
	         , os.path.join(work_dir['results'], 'ngram-mohit-no-tie.txt')
	         , save    = True )

print('\n\t>> ranking turk-no-ties with ngram graph ...')
rank_all_gold( golds['turk-no-tie']
	         , decide_fn(G)
	         , os.path.join(work_dir['results'], 'ngram-turk-no-tie.txt')
	         , save    = True )


