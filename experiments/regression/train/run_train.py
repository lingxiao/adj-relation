############################################################
# Module  : run train penalized logistic regression 
#           using neighbor features and binomial prior
# Date    : April 24th, 2017
# Author  : Xiao Ling
############################################################

import os
import pickle
from sklearn.linear_model import LogisticRegression

from app           import *
from utilities     import *
from experiments.regression import *
from experiments.regression.train import *

############################################################
'''
    Training config
'''
model = 'logistic-regression'

# logistic regression regularization
penalty    = 'l1'
C          = 0.4

# data set to train the model on
# and the size of feature represenation
data_set   = 'ppdb-ngram'
num_neigh  = 10

w2idx    = {'neig-' + str(k) : {'idx': k} \
           for k in xrange(num_neigh)}

# feature representation function
fix, nu  = 'HT' , nu_coin( graphs[data_set], num_neigh )
OP , op  = '`-`'  , vec_subtract
phi      = to_x(nu,op)

############################################################
'''
    train and validation data 
'''
if data_set == 'ppdb-ngram':
    no_data_gold = ngram_no_data
elif data_set == 'ppdb':
    no_data_gold = ppdb_no_data
elif data_set == 'ngram':
    no_data_gold = both_no_data

###########################################################
'''
    Train 
'''
dir_name = model        + '|'                                 \
         +  data_set    + '|'                                 \
         + '[nu^'+ fix  + '(s)' + OP + 'nu^' + fix + '(t)]|'  \
         + 'num_neigh=' + str(num_neigh) + '|'                \
         + 'penalty='   + penalty        + '|'                \
         + 'C='         + str(C)         + '|'                \
         + 'num_tosses=1'

print('\n\t>> Training ' + dir_name)
exec_train( dir_name = dir_name

          , model    = model

          , penalty  = penalty
          , C        = C

          , rho      = nu
          , op       = op
          , w2idx    = w2idx

          , train    = no_data_gold['bcs']
          , valid    = no_data_gold['ccb']
          , test     = no_data_gold['moh']

          , out_root = work_dir['models']
          , save     = False
          )

