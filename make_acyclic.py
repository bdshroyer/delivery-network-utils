import networkx as nx
from copy import deepcopy


def make_acyclic(G, hubs):
    if not issubclass(type(G), nx.Graph):
        raise RuntimeError("Must supply a networkx graph as input.")

    H = deepcopy(G)
    if isinstance(H, nx.Graph):
        H = H.to_directed()

    if type(hubs) != list:
        hubs = [hubs]

    for hub in hubs:
        if hub is None:
            continue
        elif hub not in list(H.nodes()):
            raise RuntimeError("Base '{}' does not exist in distribution network.".format(hub))

        hub_prime = -hub
        new_edges = list(map(lambda u: (u,hub_prime), H.predecessors(hub)))


        H.add_node(hub_prime)
        H.remove_edges_from(list(H.in_edges(hub)))
        H.add_edges_from(new_edges)

    return H
