############################################################
# Module  : MILP
# Date    : April 24th, 2017
# Author  : Xiao Ling
############################################################


from app           import *
from utilities     import *
from experiments.rank_all import *
from experiments.milp import *

print('\n>> initalization application ...')
app      = App()
work_dir = app.module( 'experiments/milp'
	                 , ['demos','results']
	                 )

print('\n>> loading gold set')
golds = read_all_gold(app.fetch('gold'))

print('\n>> loading ngram set')
ngram_dir  = app.fetch('ngrams')
word_count = [ p for p in os.listdir(ngram_dir) if 'word-count' in p ]

if word_count:
	with open(os.path.join(ngram_dir,word_count[0])) as h:
		word_count = pickle.load(h)

else:
	raise NameError('cannot find one-gram file')		

with open(os.path.join(ngram_dir, 'stat-strong-weak.pkl'), 'rb') as h:
	total_stat = pickle.load(h)


print('\n>> running MILP algorithm on dev gold-set ..'
	 '\n>> please find the results in experiments/milp/results')

decide = paper_milp(app.fetch('ngrams-milp-format'), total_stat, word_count)	

rank_all_gold( golds['dev']
	         , decide
	         , os.path.join(work_dir['results'], 'dev.txt')
	         , save = True)


print('\n>> To run on full gold sets using milp method'
	 '\n>> run scripts from experiments/milp/demos'
	 'start `python` interpretor in adj-relation directory and do, ie:'
	 '\n\t `adj-relation/experiments/milp/demos/ppdb_graph.py`')
