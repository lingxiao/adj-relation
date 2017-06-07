############################################################
# Module  : Baseline
# Date    : April 24th, 2017
# Author  : Xiao Ling
############################################################

from app           import *
from utilities     import *
from experiments.argmax import *
from experiments.rank_all import *
from experiments.baseline import *


print('\n>> initializating application ...')
app      = App()
work_dir = app.module( 'experiments/baseline'
	                 , ['demos','results']
	                 )

print('\n>> loading gold set')
golds = read_all_gold(app.fetch('gold'))

print('\n>> loading all graphs')
graphs = {
	  'ppdb'      : Graph(app.fetch('graph/ppdb'      ))
	, 'ngram'     : Graph(app.fetch('graph/ngram'     ))
	, 'ppdb-ngram': Graph(app.fetch('graph/ppdb-ngram'))
    }


print('\n>> running baseline algorithm on dev gold-set ..'
	 '\n>> please find the results in experiments/baseline/results')

rank_all_gold( golds['dev']
	         , decide_fn(graphs['ppdb'])
	         , os.path.join(work_dir['results'], 'ppdb-dev.txt')
	         , save = True)


print('\n>> To run on full gold sets using baseline method'
	 '\n>> run scripts from experiments/baseline/demos'
	 'start `python` interpretor in adj-relation directory and do, ie:'
	 '\n\t `adj-relation/experiments/baseline/demos/ppdb_graph.py`'
	 '\n>> warning: running the demos will take a while'
	 )
