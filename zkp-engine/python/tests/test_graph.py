import networkx as nx

from src.graph import (apply_isomorphism, generate_graph,
                   generate_random_permutation)


def test_generate_graph_deterministic():
    secret = b"supersecret"
    n = 10
    p = 0.5
    G1 = generate_graph(secret, n=n, p=p)
    G2 = generate_graph(secret, n=n, p=p)
    # Same secret and parameters should yield isomorphic graphs.
    assert nx.is_isomorphic(
        G1, G2
    ), "Graphs generated with the same secret should be isomorphic."


def test_generate_graph_node_count():
    secret = b"anothersecret"
    n = 15
    G = generate_graph(secret, n=n, p=0.3)
    assert G.number_of_nodes() == n, "Graph should have the expected number of nodes."


def test_generate_random_permutation_validity():
    secret = b"some_secret"
    G = generate_graph(secret)
    nodes = sorted(G.nodes())
    permutation = generate_random_permutation(G)
    # The permutation should be a rearrangement of the nodes.
    assert (
        sorted(permutation) == nodes
    ), "Permutation must contain exactly the graph's nodes."
    assert len(permutation) == len(
        nodes
    ), "Permutation length must match the number of nodes."


def test_apply_isomorphism():
    secret = b"isomorphism_test"
    G = generate_graph(secret)
    permutation = generate_random_permutation(G)
    G_iso = apply_isomorphism(G, permutation)
    # The relabeled graph should be isomorphic to the original.
    assert nx.is_isomorphic(
        G, G_iso
    ), "Graph after applying isomorphism must be isomorphic to the original."
