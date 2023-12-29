#!/usr/bin/env python3
import networkx as nx
import matplotlib.pyplot as plt
from enum import Enum, StrEnum, auto

class Player(Enum):
    Eve = auto()
    Adam = auto()

class Color(StrEnum):
    Win = "#0069b4"
    Other = "black"

# (owner, position_x, position_y)
nodes = [
        (0, {"owner": Player.Eve, "pos": (0,1)}),
        (1, {"owner": Player.Adam, "pos": (1,1)}),
        (2, {"owner": Player.Eve, "pos": (2,1)}),
        (3, {"owner": Player.Eve, "pos": (3,1)}),
        (4, {"owner": Player.Adam, "pos": (0,0)}),
        (5, {"owner": Player.Eve, "pos": (1,0)}),
        (6, {"owner": Player.Adam, "pos": (2,0)}),
        (7, {"owner": Player.Adam, "pos": (3,0)}),
        ]
edges = [
        (0, 1, {"color": Color.Other}),
        (0, 4, {"color": Color.Other}),
        (1, 2, {"color": Color.Other}),
        (1, 4, {"color": Color.Other}),
        (2, 3, {"color": Color.Other}),
        (2, 6, {"color": Color.Other}),
        (3, 2, {"color": Color.Other}),
        (3, 7, {"color": Color.Other}),
        (4, 0, {"color": Color.Other}),
        (4, 5, {"color": Color.Other}),
        (5, 5, {"color": Color.Other}),
        (5, 6, {"color": Color.Other}),
        (6, 5, {"color": Color.Other}),
        (6, 7, {"color": Color.Other}),
        (7, 7, {"color": Color.Win}),
        ]

class Game(nx.DiGraph):

    @classmethod
    def construct(cls, nodes, edges, **attr):
        obj = cls(attr)
        obj.add_nodes_from(nodes)
        obj.add_edges_from(edges)
        return obj

    def eves_nodes(self):
        return nx.subgraph_view(self, filter_node=lambda n: self.nodes[n]["owner"]==Player.Eve)

    def adams_nodes(self):
        return nx.subgraph_view(self, filter_node=lambda n: self.nodes[n]["owner"]==Player.Adam)

    def draw_nodes(self):
        node_options = {"edgecolors": "black", "node_size": 400, "node_color": "white"}

        pos = nx.get_node_attributes(self, "pos")
        nx.draw_networkx_nodes(self, pos, self.eves_nodes(), node_shape='o', **node_options)
        nx.draw_networkx_nodes(self, pos, self.adams_nodes(), node_shape='s', **node_options)

        nx.draw_networkx_labels(self, pos)

    def draw_edges(self):
        pos = nx.get_node_attributes(self, "pos")
        edge_options = {"arrowsize": 20, "node_size": 400}

        bi_edges = list(filter(lambda e: e[0] != e[1] and (e[1], e[0]) in self.edges, self.edges))
        bi_edges_colors = list(map(lambda e: self.edges[e]["color"], bi_edges))
        nx.draw_networkx_edges(self, pos, edgelist=bi_edges, edge_color=bi_edges_colors, connectionstyle='arc3,rad=0.2', **edge_options)

        single_edges = list(filter(lambda e: (e[1], e[0]) not in self.edges, self.edges))
        single_edges_colors = list(map(lambda e: self.edges[e]["color"], single_edges))
        nx.draw_networkx_edges(self, pos, edgelist=single_edges, edge_color=single_edges_colors, **edge_options)

        loop_edges = list(filter(lambda e: e[0] == e[1], self.edges))
        loop_edges_colors = list(map(lambda e: self.edges[e]["color"], loop_edges))
        nx.draw_networkx_edges(self, pos, edgelist=loop_edges, edge_color=loop_edges_colors, node_size=1000, arrowsize=20)





game = Game.construct(nodes, edges)

game.draw_nodes()
game.draw_edges()

ax = plt.gca()
ax.set_aspect('equal', 'box')
ax.set(xlim=(-1, 4), ylim=(-1, 2))
ax.axis('off')

plt.tight_layout()

plt.show()
