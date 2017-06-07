############################################################
# Module  : pointwise estimation baseline
# Date    : April 24th, 2017
# Author  : Xiao Ling
############################################################

from app           import *
from utilities     import *
from experiments.regression import *
from experiments.regression.utils import *

print('\n>> initializating application ...')
app      = App()
work_dir = app.module( 'experiments/regression'
                       , ['demos'
                         ,'results'
                         ,'train'
                         ,'models'
                         ,'w2idx']
                      )

split_gold = app.module('experiments/split-gold')

print('\n>> loading gold set')
golds = read_all_gold(app.fetch('gold'))

print('\n>> loading all graphs')
graphs = {
    'ppdb'           : Graph(app.fetch('graph/ppdb'                        ))
    , 'ngram'        : Graph(app.fetch('graph/ngram'                       ))
    , 'ppdb-ngram'   : Graph(app.fetch('graph/ppdb-ngram'                  ))
    , 'ppdb-ngram-1' : Graph(app.fetch('graph/ppdb-one-event-ngram-no-loop'))
    }


print('\n>> opening no-data gold sets ...')
ngram_no_data = { 
      'ccb': no_data_pairs(os.path.join( split_gold['no-data']
                         , 'baseline-ngram-ccb-no-data.pkl')),

      'moh': no_data_pairs(os.path.join( split_gold['no-data']
                         , 'baseline-ngram-moh-no-data.pkl')),

      'bcs': no_data_pairs(os.path.join( split_gold['no-data']
                         , 'baseline-ngram-bcs-no-data.pkl')),
     }     

ppdb_no_data = { 

      'ccb': no_data_pairs(os.path.join( split_gold['no-data']
                         , 'baseline-ppdb-ccb-no-data.pkl')) ,

      'moh': no_data_pairs(os.path.join( split_gold['no-data']
                         , 'baseline-ppdb-moh-no-data.pkl')) ,

      'bcs': no_data_pairs(os.path.join( split_gold['no-data']
                         , 'baseline-ppdb-bcs-no-data.pkl')) ,
     }     


both_no_data = { 

      'ccb': no_data_pairs(os.path.join( split_gold['no-data']
                         , 'baseline-ppdb-ngram-ccb-no-data.pkl')),

      'moh': no_data_pairs(os.path.join( split_gold['no-data']
                         , 'baseline-ppdb-ngram-moh-no-data.pkl')),

      'bcs': no_data_pairs(os.path.join( split_gold['no-data']
                         , 'baseline-ppdb-ngram-bcs-no-data.pkl')),
     }   
