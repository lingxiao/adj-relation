############################################################
# Module  : Graph Class
# Date    : April 3rd, 2017
# Author  : Xiao Ling, merle
############################################################

import os
import pickle
from utilities import *

'''

	Graph class and associated functions. 


	Class parameters:

		graph_dir :: String
				path to directory holding all graph edges.pkl files


	Class methods:

		- out_neigh :: String -> Dict String (Dict String Int)
				given vertex `src`, output dictionary of form:
					tgt:  adverb: adverb_freq

				of in neighbors and edges incident on src

		- in_neigh :: String -> Dict String (Dict String Int)
				given vertex `tgt`, output dictionary of form:
					src:  adverb: adverb_freq

				of out neighbors and edges from src

		- neigh :: String -> Dict String (Dict String Int)
					given vertex `src`, output dictionary of form:
						tgt:  adverb: adverb_freq

				of in and out neighbors 

		- edge :: String -> String -> [(String, String, String)] 
			         given vertices src and tgt, output all 
			         edges from src to tgt


'''
class Graph:

	def __init__(self, graph_dir):

		name = graph_dir.split('/')[-1]
		print('\n\t>> constructing graph ' + name + ' ...')

		E,V = load_as_dict(graph_dir)

		self.edges    = E
		self.vertices = V


	############################################################
	'''
		graph topology
	'''

	def out_neigh(self,src):
		E = self.edges
		if src in E:
			return E[src]
		else:
			return dict()

	'''
		@Use: given target `tgt`, get all parents of tgt and
			  the edge from parent to target
	'''
	def in_neigh(self,tgt):

		E = self.edges
		if tgt in E:
			return { _s :_d[tgt] for _s,_d in E.iteritems() if tgt in _d } 
		else:
			return dict()

	'''
		@Use: output in and out neighbors
	'''
	def neigh(self,src):
		in_vs  = self.in_neigh(src)
		out_vs = self.out_neigh(src)

		return { k:v for k,v in list(in_vs.iteritems()) + list(out_vs.iteritems()) }


	############################################################
	'''
		edge and ppr meaures
	'''

	'''
		@use: given vertices s and t
		 	  output raw edges between them, and weight of edge
	'''
	def edge(self,src,tgt):

		E = self.edges

		if src in E:
			if tgt in E[src]: 
				return E[src][tgt]
			else:
				return dict()
		else:
			raise NameError('Error: ' + s + ' no in graph')



############################################################
'''
	@Use: given path to graph, open edge as form:
		  	word_s:
		  		word_s_1: 
		  			adv_1: count
		  			adv_2  count
		  			...
		  		word_s_2
		  		...
		  	so that we have, ie for edge set `E`
				E['good']['great']['<very'>] = 100
	@Input: path  :: String
	@output: (edges,vertices) :: Dict String (Dict String (Dict String Int))
	                           , [String]
'''
def load_as_dict(path):

	if os.path.isdir(path):

		paths = [os.path.join(path,p) for p in os.listdir(path)]

		E = []
		V = []

		for path in paths:

			es,vs = load_as_dict(path)
			E += [(k,v) for k,v in es.iteritems()]
			V  += vs

		all_E = {k : v for k,v in E}

		return all_E, list(set(V))

	elif os.path.isfile(path):

		_,ext = path.split('.')

		if ext == 'pkl':
			with open(path,'rb') as h:
				G = pickle.load(h)

				return G['edge'], G['vertex']

		else:
			raise NameError("expected pkl file")

	else:
		raise NameError("expected pkl file or directory of pkl file")

