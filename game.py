#!/usr/bin/env python3
import networkx as nx
import matplotlib.pyplot as plt
from enum import Enum, StrEnum, auto

class Player(Enum):
    Eve = auto()
    Adam = auto()

Eve = Player.Eve
Adam = Player.Adam

class Color(StrEnum):
    Win = "#0069b4"
    Other = "black"

# (owner, position_x, position_y)
nodes = [
        (0, {"owner": Eve, "pos": (0,0)}),
        (1, {"owner": Eve, "pos": (0,1)}),
        (2, {"owner": Adam, "pos": (1,0)}),
        (3, {"owner": Adam, "pos": (1,1)}),
        ]
edges = [
        (0, 1, {"color": Color.Win}),
        (0, 2, {"color": Color.Other}),
        (1, 3, {"color": Color.Other}),
        (2, 3, {"color": Color.Other}),
        ]

game = nx.DiGraph()
game.add_nodes_from(nodes)
game.add_edges_from(edges)

eve_nodes = nx.subgraph_view(game, filter_node=lambda n: game.nodes[n]["owner"]==Eve)
adam_nodes = nx.subgraph_view(game, filter_node=lambda n: game.nodes[n]["owner"]==Adam)


pos = nx.get_node_attributes(game, "pos")
print(game.edges(data=True))
edge_colors = [c for (u,v,c) in game.edges.data('color')]

node_options = {"edgecolors": "black", "node_size": 400, "node_color": "white"}
nx.draw_networkx_nodes(game, pos, eve_nodes, node_shape='o', **node_options)
nx.draw_networkx_nodes(game, pos, adam_nodes, node_shape='s', **node_options)
nx.draw_networkx_edges(game, pos, edge_color=edge_colors, )



plt.axis("off")
plt.tight_layout()
plt.show()
