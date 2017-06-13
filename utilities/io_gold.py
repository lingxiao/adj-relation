############################################################
# Module  : Read and write Gold IO scripts
# Date    : December 22nd
# Author  : Xiao Ling
# ############################################################

import os


############################################################
'''
  @Use: load all gold sets
      - dev
      - mohit
      - mohit-no-tie
      - turk
      - turk-no-tie
      - base-comparative-superlative

  @Input : absolute path to gold directory    

  @Output: dictionary with keys:
        - dev
        - mohit
        - mohit-no-tie
        - turk
        - turk-no-tie
        - bcs

        and corresponding gold set with type :: [[[String]]]
        ie: 
          [ [[good,ok],[great],[superb]]
          , [[bad],[terrible]]
          ]
        means:
          good = ok < great < superb
          bad < terrible

  @ Dependency: `gold_dir` directory should have structure:
        - moh.txt
        - moh-no-tie.txt
        - turk.txt
        - turk-no-tie.txt
        - bcs
            - base-comparative.txt
            - base-superlative.txt
            - comparative-superlative.txt

'''
def read_all_gold(gold_dir):

  try:
    paths = [ os.path.join(gold_dir,p) for p in os.listdir(gold_dir) \
              if 'DS_Store' not in p ]

    dev_path         = [p for p in paths if 'dev.txt' in p ]
    turk_path        = [p for p in paths if 'turk.txt' in p]          
    moh_path         = [p for p in paths if 'moh.txt'  in p]          
    turk_path_no_tie = [p for p in paths if 'turk-no-tie.txt' in p]          
    moh_path_no_tie  = [p for p in paths if 'moh-no-tie.txt'  in p]          
    bcs_dir          = [p for p in paths if 'bcs' in p]

    if dev_path:
      print('\n\t>> loading dev set')
      dev = read_gold(dev_path[0])
    else: 
      raise NameError('cannot locate gold set : dev.txt')

    if turk_path: 
      print('\n\t>> loading turk')
      turk = read_gold(turk_path[0])
    else: 
      raise NameError('cannot locate gold set : turk.txt')

    if moh_path:
      print('\n\t>> loading mohit')
      moh = read_gold(moh_path[0])
    else: 
      raise NameError('cannot locate gold set : mohit.txt')

    if turk_path_no_tie: 
      print('\n\t>> loading turk no tie')
      turk_no_tie = read_gold(turk_path_no_tie[0])
    else: 
      raise NameError('cannot locate gold set : turk-no-tie.txt')

    if moh_path_no_tie:
      print('\n\t>> loading mohit no tie')
      moh_no_tie = read_gold(moh_path_no_tie[0])
    else: 
      raise NameError('cannot locate gold set : mohit-no-tie.txt')

    if bcs_dir:
      print('\n\t>> loading base-comparative-superlative')
      bcs_paths = [os.path.join(bcs_dir[0],p) for p \
                   in os.listdir(bcs_dir[0]) \
                   if 'DS_Store' not in p ]

      bcs = []             

      for bcs_path in bcs_paths:
        with open(bcs_path,'rb') as h:
          for line in h:
            line = line.replace('\n','')
            pair = line.split(' ')
            if len(pair) == 2:
              s,t = pair
              bcs.append([[s],[t]])
    else:
      raise NameError('cannot locate gold set directory: base-comparative-superlative')

    
    out = {  'dev'         : dev
           , 'mohit'       : moh
           , 'turk'        : turk
           , 'mohit-no-tie': moh_no_tie
           , 'turk-no-tie' : turk_no_tie
           , 'bcs'         : bcs
          }

    return out      

  except:
    raise NameError("cannot locat directory with gold set")   

############################################################
'''
	@Use: read gold test set
'''
def read_gold(path):
  gold = open(path,'r').read().split('===')[1:-1]
  gold = [rs.split('\n') for rs in gold if rs.split('\n')]
  gold = [rs[1:-1] for rs in gold]
  gold = [[r.split(', ') for r in val] for val in gold]
  gold = [[[w.strip() for w in ws] for ws in cluster] for cluster in gold]
  return gold

'''
  @Use: write gold test so that
        read_gold(p) == (write_gold q golds >>=\q -> read_gold(q))
'''
def write_gold(path, golds):
  with open(path, 'wb') as h:
    for gold in golds:
      h.write('=== foo, bar'  + '\n')
      for ws in gold:
        h.write(', '.join(ws) + '\n')
    h.write('=== END')
    h.close()
    return path
