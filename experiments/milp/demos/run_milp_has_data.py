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


gold_root       = app.fetch('gold')
turk_ngram_data = os.path.join(gold_root, 'turk-has-ngram-data.txt')
bcs_ngram_data  = os.path.join(gold_root, 'bcs-has-ngram-data.txt' )

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


