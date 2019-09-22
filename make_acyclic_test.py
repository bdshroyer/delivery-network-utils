import pytest
import make_acyclic as ma
import networkx as nx

@pytest.fixture
def empty_digraph():
    return nx.DiGraph()

@pytest.fixture
def simple_cyclic_digraph():
    G = nx.DiGraph()
    G.add_nodes_from([1,2,3])
    G.add_edges_from([(1,2), (1,3), (2,1), (3,1)])
    return G

@pytest.fixture
def multihub_cyclic_digraph():
    G = nx.DiGraph()
    G.add_nodes_from([1,2,3,4])
    G.add_edges_from([(1,2), (1,3), (2,1), (3,1), (4,2), (4,3), (2,4), (3,4)])
    return G

@pytest.fixture
def simple_cyclic_digraph_hub():
    return 1

@pytest.fixture
def mulithub_cyclic_digraph_hubs():
    return [1, 4]

@pytest.fixture
def simple_unfolded_digraph():
    G = nx.DiGraph()
    G.add_nodes_from([1,2,3,-1])
    G.add_edges_from([(1,2), (1,3), (2,-1), (3,-1)])
    return G

@pytest.fixture
def simple_acyclic_digraph():
    G = nx.DiGraph()
    G.add_nodes_from([1,2,3,4])
    G.add_edges_from([(1,2), (1,3), (2,4), (3,4)])
    return G

@pytest.fixture
def multihub_unfolded_digraph():
    G = nx.DiGraph()
    G.add_nodes_from([1,2,3,-1])
    G.add_nodes_from([1,2,3,4,-1,-4])
    G.add_edges_from([(1,2), (1,3), (2,-1), (3,-1), (4,2), (4,3), (2,-4), (3,-4)])
    return G

# Happy path--Given a cyclic digraph and a hub node, returns an unfolded DAG
def test_make_acyclic_single(simple_cyclic_digraph, simple_cyclic_digraph_hub, simple_unfolded_digraph):
    G = ma.make_acyclic(simple_cyclic_digraph, simple_cyclic_digraph_hub)
    assert G.nodes == simple_unfolded_digraph.nodes
    assert G.edges == simple_unfolded_digraph.edges

# If no hub node is provided, returns the input graph
def test_make_acyclic_noop(simple_cyclic_digraph, simple_unfolded_digraph):
    G = ma.make_acyclic(simple_cyclic_digraph, None)
    assert G.nodes == simple_cyclic_digraph.nodes
    assert G.edges== simple_cyclic_digraph.edges

# Given an empty digraph and a no-op, returns the empty digraph
def test_make_acyclic_empty(empty_digraph):
    G = ma.make_acyclic(empty_digraph, None)
    assert G.nodes == empty_digraph.nodes
    assert G.edges== empty_digraph.edges

# Given an hub not in the given graph, raises an error
def test_make_acyclic_empty(simple_cyclic_digraph):
    fake_hub = max(list(simple_cyclic_digraph.nodes)) + 1
    with pytest.raises(RuntimeError) as rte:
        ma.make_acyclic(simple_cyclic_digraph, fake_hub)
    assert "Hub '{}' does not exist in distribution network.".format(fake_hub) in str(rte.value)

# Raises an error if a non-graph is provided
def test_make_acyclic_a_graph():
    with pytest.raises(RuntimeError) as rte:
        ma.make_acyclic(None, None)
    assert "Must supply a networkx digraph as input." in str(rte.value)

# Acts as a no-op on a DAG
def test_make_acyclic_acyclic(simple_acyclic_digraph, simple_cyclic_digraph_hub):
    G = ma.make_acyclic(simple_acyclic_digraph, simple_cyclic_digraph_hub)
    assert G.nodes == simple_acyclic_digraph.nodes
    assert G.edges == simple_acyclic_digraph.edges

# Raises an error on an undirected graph
def test_make_acyclic_undirected(simple_cyclic_digraph, simple_cyclic_digraph_hub, simple_unfolded_digraph):
    with pytest.raises(RuntimeError) as rte:
        ma.make_acyclic(simple_cyclic_digraph.to_undirected(), simple_cyclic_digraph_hub)
    assert "Must supply a directed graph as input." in str(rte.value)

# Happy path--Given a cyclic digraph and a list of hub nodes, returns an unfolded DAG
def test_make_acyclic_multihub(multihub_cyclic_digraph, mulithub_cyclic_digraph_hubs, multihub_unfolded_digraph):
    G = ma.make_acyclic(multihub_cyclic_digraph, mulithub_cyclic_digraph_hubs)
    assert G.nodes == multihub_unfolded_digraph.nodes
    assert G.edges == multihub_unfolded_digraph.edges

