############################################################
# Module  : train elastic net regression
# Date    : April 24th, 2017
# Author  : Xiao Ling
############################################################

import os
import math
import numpy as np
from sklearn.linear_model import LogisticRegression
import pickle

from app     import *
from utilities     import *
from experiments.regression import *
from experiments.rank_all import *

############################################################
'''
	@Use: train validate and test model. save results if needed
'''
def exec_train( dir_name = None

	          , model    = ''

	          , penalty    = ''
	          , C          = None

	          , rho      = None
	          , op       = None
	          , w2idx    = None

	          , train    = None
	          , valid    = None
	          , test     = None

	          , out_root = None
	          , save     = False ):

	train_X, train_y, train_gold = train
	valid_X, valid_y, valid_gold = valid
	test_X , test_y , test_gold  = test
	
	X   = to_X(train_X, rho, op)
	y   = np.array(train_y)
	phi = to_x(rho, op)


	print('\n\t>> training model ' + model + ' ...')
	
	print('\n\t >> running ' + model + ' with penalty ' + penalty + ' at C = ' + str(C))
	model = LogisticRegression(C = C, penalty = penalty)
	model = model.fit(X, y)
	decide = decide_fn_model_Binomial(model, phi)


	print('\n\t>> decoding coefficients of model')
	vector = model.coef_

	if len(vector) == len(w2idx):
		coefs  = decode(vector,w2idx)		
		print('\n\t>> coefficents: ')
		for w,v in coefs.iteritems():
			print('\n\t\t ' + w + ': ' + str(v))
	else:
		coefs = {k:c for k,c in enumerate(vector)}
		print('\n\t\t >> coefficents: ' + str(coefs))


	print('\n\t>> ranking bcs ...')
	rank_all_gold( train_gold
		         , decide
		         , ''
		         , save    = False )

	print('\n\t>> ranking turk ...')
	rank_all_gold( valid_gold
		         , decide
		         , ''
		         , save    = False )

	print('\n\t>> ranking moh ...')
	rank_all_gold( test_gold
		         , decide
		         , ''
		         , save    = False )

	if save:

		results_dir = os.path.join(out_root, dir_name)

		print('\n\t>> saving results to ' + dir_name)
		if not os.path.exists(results_dir):
			os.mkdir(results_dir)		

		m_path = os.path.join( results_dir, 'model' )

		print('\n\t>> saving model ')
		pickle.dump(model, open(m_path, 'wb'))	

		print('\n\t>> saving coefficients ...')
		with open(os.path.join(results_dir, 'coef.txt'),'wb') as h:
			for v,n in coefs.iteritems():
				h.write(str(v) + ': ' + str(n) + '\n')		












