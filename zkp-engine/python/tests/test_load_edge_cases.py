import time

import networkx as nx
import pytest

from src.graph import (apply_isomorphism, generate_graph,
                   generate_random_permutation)
from src.protocol import execute_protocol
from src.rotation import rotate_graph


def test_graph_n_zero():
    """Edge Case: Generate a graph with 0 nodes; expect an empty graph."""
    secret = b"edge_secret"
    G = generate_graph(secret, n=0, p=0.5)
    assert G.number_of_nodes() == 0, "Graph with 0 nodes should be empty."


def test_graph_n_one():
    """Edge Case: Generate a graph with 1 node; expect a single node and no edges."""
    secret = b"edge_secret"
    G = generate_graph(secret, n=1, p=0.5)
    assert G.number_of_nodes() == 1, "Graph with 1 node should have exactly 1 node."
    assert G.number_of_edges() == 0, "Graph with 1 node should have 0 edges."


def test_graph_p_zero():
    """Edge Case: With p=0, the graph should have no edges (isolated nodes)."""
    secret = b"edge_secret"
    n = 10
    G = generate_graph(secret, n=n, p=0.0)
    assert G.number_of_edges() == 0, "Graph with p=0 should have 0 edges."


def test_graph_p_one():
    """Edge Case: With p=1, the graph should be complete."""
    secret = b"edge_secret"
    n = 10
    G = generate_graph(secret, n=n, p=1.0)
    expected_edges = n * (n - 1) // 2
    assert (
        G.number_of_edges() == expected_edges
    ), f"Graph with p=1 should have {expected_edges} edges."


def test_large_graph_generation():
    """Load Test: Generate a larger graph to simulate load and ensure performance."""
    secret = b"load_secret"
    n = 500  # Adjust based on your system's capacity.
    p = 0.1
    start = time.time()
    G = generate_graph(secret, n=n, p=p)
    duration = time.time() - start
    assert (
        G.number_of_nodes() == n
    ), "Large graph should have the specified number of nodes."
    assert duration < 1, "Graph generation should complete in under 1 second."


def test_protocol_load():
    """Load Test: Execute the protocol for 100 rounds to simulate load."""
    secret = b"protocol_load"
    n = 10
    p = 0.5
    G1 = generate_graph(secret, n=n, p=p)
    secret_iso = generate_random_permutation(G1)
    G2 = apply_isomorphism(G1, secret_iso)
    result = execute_protocol(G1, G2, secret_iso, rounds=100)
    assert result, "Protocol should succeed under a heavy load of rounds."


def test_invalid_graph_parameters():
    """Edge Case: Ensure invalid parameters raise errors."""
    secret = b"invalid_secret"
    # Negative number of nodes should raise ValueError.
    with pytest.raises(ValueError):
        generate_graph(secret, n=-5, p=0.5)
    # p < 0 should raise ValueError.
    with pytest.raises(ValueError):
        generate_graph(secret, n=10, p=-0.1)
    # p > 1 should raise ValueError.
    with pytest.raises(ValueError):
        generate_graph(secret, n=10, p=1.1)


def test_deterministic_permutation_with_seed():
    """Edge Case: With a given seed, the permutation should be deterministic."""
    secret = b"deterministic_secret"
    G = generate_graph(secret, n=10, p=0.5)
    seed = 123456
    perm1 = generate_random_permutation(G, seed=seed)
    perm2 = generate_random_permutation(G, seed=seed)
    assert perm1 == perm2, "Permutations with the same seed must be identical."
