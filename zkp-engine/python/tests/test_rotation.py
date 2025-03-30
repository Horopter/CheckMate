import networkx as nx

from src.graph import generate_graph
from src.rotation import rotate_graph


def test_rotate_graph_produces_new_graph():
    secret = b"rotate_secret"
    nonce = b"unique_nonce_12345"
    n = 10
    p = 0.5
    original_graph = generate_graph(secret, n=n, p=p)

    new_G1, new_secret_iso = rotate_graph(secret, nonce, n=n, p=p)
    # Ensure new_G1 is a valid graph.
    assert isinstance(new_G1, nx.Graph), "Rotation must produce a valid graph."
    # new_secret_iso should be a permutation of new_G1's nodes.
    nodes = sorted(new_G1.nodes())
    assert (
        sorted(new_secret_iso) == nodes
    ), "New secret isomorphism must be a valid permutation of graph nodes."


def test_rotate_graph_determinism_with_same_nonce():
    secret = b"rotate_secret_same"
    nonce = b"same_nonce"
    n = 10
    p = 0.5
    new_G1_a, new_secret_iso_a = rotate_graph(secret, nonce, n=n, p=p)
    new_G1_b, new_secret_iso_b = rotate_graph(secret, nonce, n=n, p=p)
    # With the same secret and nonce, the rotation should yield identical outputs.
    assert nx.is_isomorphic(
        new_G1_a, new_G1_b
    ), "Rotated graphs with same parameters should be isomorphic."
    assert (
        new_secret_iso_a == new_secret_iso_b
    ), "Secret isomorphisms should be identical with the same nonce."


def test_rotate_graph_different_nonce():
    secret = b"rotate_secret_diff"
    nonce_a = b"nonce_a"
    nonce_b = b"nonce_b"
    n = 10
    p = 0.5
    new_G1_a, new_secret_iso_a = rotate_graph(secret, nonce_a, n=n, p=p)
    new_G1_b, new_secret_iso_b = rotate_graph(secret, nonce_b, n=n, p=p)
    # Although graphs may be isomorphic by chance, secret isomorphism permutations should differ.
    assert (
        new_secret_iso_a != new_secret_iso_b
    ), "Different nonces should yield different secret isomorphisms."
