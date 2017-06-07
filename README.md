# Code base for the TACL Paper [TO BE NAMED]

## Dependencies
* python 2.7.13
* yaml
* pulp
* numpy
* sklearn

## Instructions:

1. Make sure all dependencies are installed
3. Download the data for this experiment at [link/to/data] and place in directory `path/to/data`
3. Git clone this repo to `path/to/adj-relation`
4. Change the `local` field in adj-relation/config.yml file to `path/to/data`
5. Open bash and set the path by:

```
export PYTHONPATH=/path/to/adj-relation
```
6. Finally, `cd` into `path/to/adj-relation`. Note this repo contains all pre-run results in their respective experiments subdirectory (see below). To re-run experiments:

* Run random baseline, run this command in bash:

```python
python experiments/baseline/demos/uniform.py
```

You may find the results at experiments/baseline/results

* Run non-random baseline for each data set:

```python
python experiments/baseline/demos/ppdb_graph.py
python experiments/baseline/demos/ngram_graph.py
python experiments/baseline/demos/ppdb_ngram_graph.py
```

You may find the results at experiments/baseline/results


* Run logistic regression for each data set:

```python
python experiments/regression/demos/run_model_redo.py
```

You may find the results at experiments/regression/results


* Run my replication of Mohit's MILP method:

```python
python experiments/regression/demos/run_milp.py
```

You may find the results at experiments/milp/results


Warning: re-running these experiments takes a long time.


## Contact.

lingxiao . at . seas . upenn . edu





