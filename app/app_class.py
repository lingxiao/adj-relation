############################################################
# Module  : Application class
# Date    : March 23rd, 2017
# Author  : Xiao Ling
############################################################

import os
import yaml
import shutil
import pickle
import collections

from app import *

############################################################
'''
  ============
   App Class
  ============

  @Use: Initialize application and get all directory paths
  
  @Dependencies: expects configuration file located at
                  [ adj-relation/config.yml ]

                 with fields:
                    data:
                        local: 
                        grid:

  @methods:

    fetch: given path or relative path to directory
           output absolute path if it exists

    module: Given name of module 
            initialize module and make all subdirectory if it does not exist
            else output all subdirectory absolute paths
            by defualt module will have files:
              __init__.py
              top.py

   shard_data: given path to data, create file with paths
               to data, sharded by alphbetical order

  ==========================================================
'''
class App:

  def __init__(self):

    root     = os.getcwd   ()
    env_path = os.path.join( root, 'config.yml')

    # read application configuration
    print('\n\t>> loading application config ...')
    with open(env_path, 'r') as h:
      try:
        env = yaml.load(h)
      except yaml.YAMLError as e:
        print e

    # crawl current app for all directories
    print('\n\t>> loading all code paths')
    ENV = get_all_paths(root)

    for k,p in flatten(env).iteritems():
      if k not in ENV:
        ENV[k] = p

    # crawl data directory for current app 
    # for all directories
    print('\n\t>> loading all data paths, this will take a minute ...')

    data_root = locate_data_root(ENV, root)

    denv  = { 'data/' + n : p for n,p in     \
            get_all_paths(data_root).iteritems() }

    for k,p in denv.iteritems():
      if k not in ENV:
        ENV[k] = p

    # save environmental variables
    self.ENV = ENV

  def fetch(self, name):
    return fetch_path(self.ENV, name)

  def module(self, name, subdirs = []):
    return make_dirs(get_path(self.ENV, name), subdirs)


############################################################
'''
  @Use: select right data directory to use based on path
'''
def locate_data_root(ENV, root):

  # local
  if root[0:6] == '/Users':
    droot = 'data/local'

  # enaic or nlpgrid
  elif root[0:5] == '/mnt/':
    if os.path.exists(ENV['data/grid']):
      droot = 'data/grid'
    else:
      droot = 'data/eniac'

  return ENV[droot]

'''
  @Use: get path to module name if it exists
        otherwise output app-root/name
'''
def get_path(PATH, name):

  out = None

  try:
    out = fetch_path(PATH, name)
  except:
    if 'data' in name:
      pass
    else:
      out = os.path.join(PATH['root'], name)

  return out


'''
  @Use: get path to module name if it exists
        otherwise raise error
'''
def fetch_path(PATH, name):

  keys  = [k for k in PATH if name in k]
  keys.sort()
  keys  = [keys[0]] if len(keys) >= 1 else []
  names = [n for n in [name] + keys if n in PATH]

  if names:
    return PATH[names[0]]
  else:
    raise NameError('Error: cannot locate path named: ' + name)

'''
  @Use: given dictionary, flatten all key value pairs
'''
def flatten(d, parent_key='', sep='/'):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

############################################################
'''
  @Use: given root, traverse find all subdirectories
        and make 
          name: path
        dictionary
        note if two distinct subdirectory have respective 
        subdirectories with the same name, the first 
        one is is overridden by the second one
'''
def get_all_paths(root):
  return { to_name(root, d):  d for d,_,_ in os.walk(root) }

'''
  @Use: make name of path `root/path/to/dir` `path/to/dir`
'''
def to_name(root, path):

  name = path.replace(root,'')
  if name:
    return name[1:]
  else:
    return 'root'
############################################################
'''
  @Use: given absolute path `root` to directory
        make all subdirs if not refresh
        else grab the subdirs if the exists
'''
def make_dirs(root, subdirs):

  if not os.path.exists(root):

    print('\n\t>> making root directory at ' + root)
    os.mkdir(root)

    print('\n\t>> adding init file')
    with open(os.path.join(root,'__init__.py'),'wb') as h:
      h.write('# auto generated init file\n\nfrom .top import *')

    print('\n\t>> adding top file')
    name    = root.split('/')[-1]
    content = header.replace ('{MODULE}', name )
    content = content.replace("{DATE}"  , time.strftime("%m/%d/%Y") )

    with open(os.path.join(root,'top.py'),'wb') as h:
      h.write(content)

  return make_subdirs(root, subdirs)

def make_subdirs(root, subdirs):

    paths   = dict()
    subs    = [p for p in os.listdir(root) if '.' not in p]
    subdirs = set(subdirs + subs)

    for subdir in subdirs:

      path = os.path.join(root, subdir)

      if os.path.exists(path):
        print('\n\t>> sub-directory already exists at ' + subdir)
        paths[subdir] = path
      else:
        print('\n\t>> making sub-directory at ' + root + '/' + subdir)
        os.mkdir(path)
        paths[subdir] = path

    paths['root'] = root

    return paths

'''
  @Use: template top.py file should have default header and path setup
'''
_mk_dir_ = '\n############################################################' \
         + "\n'''"                      \
         + "\n\tmake current directory" \
         + "\n'''"                      \
         + "\napp   = App()"            \
         + "\npaths = app.module('{MODULE}')"

header = '############################################################\n'  \
       + '# Module  : {MODULE}/top\n'                                      \
       + '# Date    : {DATE}\n'                                            \
       + '# Author  : Xiao Ling\n'                                         \
       + '############################################################\n\n'\
       + 'import os\n'                                                     \
       + 'import pickle\n'                                                 \
       + 'from app import *\n\n'                                           \
       + _mk_dir_


