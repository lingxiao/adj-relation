from __future__ import division  # For float division.
import json


import networkx
from networkx import NetworkXNoPath
from networkx.algorithms import shortest_path
from networkx.readwrite import json_graph

# import graphviz #THIS LINE MUST BE COMMENTED OUT DURING PRODUCTION
import pydot

class Graph:

    def __init__(self):
        self.nx_graph = networkx.MultiDiGraph()

    @staticmethod
    def from_json(json_filename):
        """
        Load graph from JSON file.
        :param json_filename: JSON filename.
        :return: A NetworkX graph.
        """
        with open(json_filename, 'r') as infile:
            data = json.load(infile)
            nx_graph = json_graph.node_link_graph(data)
            graph = Graph()
            graph.nx_graph = nx_graph
            return graph

    @staticmethod
    def bfs_to_json(self, src_adj, num_edges):
        """
        Save subgraph as txt file, which can be given to Parker's graph
        visualization software. To find the subgraph, perform a
        breadth-first search beginning at src_adj and continue until
        num_edges edges have been traversed.
        :param src_adj: the adjective from which to start the BFS.
        :param num_edges: the number of edges in the subgraph.
        Return formatted edges in string form.
        """
        num_edges = int(num_edges)

        bfs_vertex_pairs = networkx.bfs_edges(self.nx_graph, src_adj)

        output = []
        i = 0
        for v0, v1 in bfs_vertex_pairs:
            # Check for edges (v0, v1).
            if i < num_edges:
                if v0 in self.nx_graph and v1 in self.nx_graph[v0]:
                    edges = self.nx_graph[v0][v1]
                    adverbs = []
                    for edge_dict in edges.itervalues():
                        adverb = edge_dict['adv']
                        adverbs.append(adverb)
                    output.append(
                        {
                            "source": "%s" % v0,
                            "target": "%s" % v1,
                            "relationshipWord": "%s" % '; '.join(adverbs)
                        }
                    )
                    i += 1
            # Check for edges (v1, v0).
            if i < num_edges:
                if v1 in self.nx_graph and v0 in self.nx_graph[v1]:
                    edges = self.nx_graph[v1][v0]
                    adverbs = []
                    for edge_dict in edges.itervalues():
                        adverb = edge_dict['adv']
                        adverbs.append(adverb)
                    output.append(
                        {
                            'source': v1,
                            'target': v0,
                            'relationshipWord': '; '.join(adverbs)
                        }
                    )
                    i += 1

        return json.dumps(output)

    @staticmethod
    def subgraph_to_json(self, adj_list):
        output = []

        for src in adj_list:
            for dest in adj_list:
                if src in self.nx_graph and dest in self.nx_graph:
                    try:
                        path = shortest_path(self.nx_graph, src, dest)
                        for i in range(0, len(path) - 1):
                            v0 = path[i]
                            v1 = path[i + 1]
                            edges = self.nx_graph[v0][v1]
                            adverbs = []
                            for edge_dict in edges.itervalues():
                                adverb = edge_dict['adv']
                                adverbs.append(adverb)
                            output.append(
                                {
                                    'source': v0,
                                    'target': v1,
                                    'relationshipWord': '; '.join(adverbs)
                                }
                            )
                    except NetworkXNoPath as e:
                        print str(e)

        return json.dumps(output)

    def num_vertices(self):
        return len(self.nx_graph.nodes())

    def num_edges(self):
        return len(self.nx_graph.edges())

    def num_vertex_pairs(self):
        undirected_graph = networkx.Graph(self.nx_graph)
        return len(undirected_graph.edges())

    def num_adverbs(self):
        adverbs = set([edge[2]['adv'] for edge in self.nx_graph.edges(data=True)])
        return len(adverbs)

