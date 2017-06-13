############################################################
# Module  : combine models
# Date    : April 24th, 2017
# Author  : Xiao Ling
############################################################

from app           import *
from utilities     import *
from experiments.rank_all import *
from experiments.milp import *

############################################################
'''
	run on all data set
'''
decide      = paper_milp(app.fetch('ngrams-milp-format'), total_stat, word_count)	
SAVE        = True
results_dir = work_dir['results']

print('\n\t>> ranking mohit with milp ...')
rank_all_gold( golds['mohit']
	         , decide
	         , os.path.join(results_dir, 'mohit.txt')
	         , save = SAVE )

print('\n\t>> ranking mohit-no-ties milp ...')
rank_all_gold( golds['mohit-no-tie']
	         , decide
	         , os.path.join(results_dir, 'mohit-no-tie.txt')
	         , save = SAVE )

print('\n\t>> ranking turk with milp ...')
rank_all_gold( golds['turk']
	         , decide
	         , os.path.join(results_dir, 'turk.txt')
	         , save = SAVE )

print('\n\t>> ranking turk-no-ties milp ...')
rank_all_gold( golds['turk-no-tie']
	         , decide
	         , os.path.join(results_dir, 'turk-no-tie.txt')
	         , save = SAVE )

print('\n\t>> ranking bcs with milp ...')
rank_all_gold( golds['bcs']
	         , decide
	         , os.path.join(results_dir, 'bcs.txt')
	         , save = SAVE )




	





