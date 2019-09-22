import networkx as nx
from copy import deepcopy


def make_acyclic(G, hubs):
    """
    Returns a directed acyclic graph H, which is a version of G subject to the following modifications:
    * H is directed and acyclic, even if G is not.
    * Every node n in hubs (which should be a subset of G) has a "shadow" nprime in H.
    * Every edge in G that is inbound to a node n in hubs is now inbound to its shadow nprime in H so that:
     * Every hub node n in H has an in-degree of 0.
     * Every shadow node nprime in H has an out-degree of 0.
     * out-degree(n in H) == out-degree(n in G).
     * in-degree(nprime in H) == in-degree(n in G).

    make_acyclic raises an error if:
    * G is not a networkx graph
    * Some node n in hubs does not exist in G.
    """
    if not issubclass(type(G), nx.Graph):
        raise RuntimeError("Must supply a networkx digraph as input.")
    elif not issubclass(type(G), nx.DiGraph):
        raise RuntimeError("Must supply a directed graph as input.")

    H = deepcopy(G)

    if nx.algorithms.dag.is_directed_acyclic_graph(H):
        return H

    if type(hubs) != list:
        hubs = [hubs]

    for hub in hubs:
        if hub is None:
            continue
        elif hub not in list(H.nodes()):
            raise RuntimeError("Hub '{}' does not exist in distribution network.".format(hub))

        hub_prime = -hub
        new_edges = list(map(lambda u: (u,hub_prime), H.predecessors(hub)))

        H.add_node(hub_prime)
        H.remove_edges_from(list(H.in_edges(hub)))
        H.add_edges_from(new_edges)

    return H
