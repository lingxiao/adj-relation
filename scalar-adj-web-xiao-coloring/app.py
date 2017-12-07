from os.path import dirname

from flask import Flask, redirect, render_template, url_for

from models.graph import Graph


MYDIR = dirname(__file__)

app = Flask(__name__)
app.secret_key = 'dawoe90r2j3z8sd982jdsa'
IMAGES_MAX_AGE = 0

graph = Graph.from_json('input/graph.json')


@app.route('/')
def index():
    return render_template('index.html', num_vertices=graph.num_vertices(),
                           num_edges=graph.num_edges(),
                           num_vertex_pairs=graph.num_vertex_pairs(),
                           num_adverbs=graph.num_adverbs())


@app.route('/choose-adjectives')
def choose_adjectives():
    return redirect(url_for('view_adjectives', src_adj='happy', size=100))


@app.route('/view-adjectives/<src_adj>/<size>')
def view_adjectives(src_adj, size):
    return render_template('view-adjectives.html', src_adj=src_adj, size=size,
                           active="choose-adjectives")


@app.route('/choose-adjective-subgraph')
def choose_adjective_subgraph():
    return redirect(url_for('view_adjective_subgraph',
                            adj_list='good.great.excellent'))


@app.route('/view-adjective-subgraph/<adj_list>')
def view_adjective_subgraph(adj_list):
    adj_list_string = ', '.join(adj_list.split('.'))
    return render_template('view-adjective-subgraph.html', adj_list=adj_list,
                           adj_list_string=adj_list_string,
                           active="choose-adjectives")


@app.route('/get/adjectives/<src_adj>/<size>', methods=['GET'])
def get_adjectives(src_adj, size):
    return graph.bfs_to_json(graph, src_adj, size)


@app.route('/get/adjective-subgraph/<adj_list>', methods=['GET'])
def get_adjective_subgraph(adj_list):
    adj_list = adj_list.split('.')
    return graph.subgraph_to_json(graph, adj_list)


if __name__ == '__main__':
    # Reload on code changes. MUST be false in production.
    app.debug = False
    app.run()
