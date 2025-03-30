import networkx as nx
from hypothesis import given, settings
from hypothesis import strategies as st

# Import functions from our src modules
from src.graph import (apply_isomorphism, generate_graph,
                   generate_random_permutation)
from src.protocol import execute_protocol
from src.rotation import rotate_graph


# Fuzz test for graph generation:
@given(
    secret=st.binary(min_size=1, max_size=32),
    n=st.integers(min_value=1, max_value=50),
    p=st.floats(min_value=0.0, max_value=1.0, allow_infinity=False, allow_nan=False),
)
def test_generate_graph_fuzz(secret, n, p):
    # Given random parameters, generate_graph should produce a graph with exactly n nodes.
    G = generate_graph(secret, n=n, p=p)
    assert G.number_of_nodes() == n


# Fuzz test for generating a random permutation:
@given(
    secret=st.binary(min_size=1, max_size=32), n=st.integers(min_value=1, max_value=50)
)
def test_generate_random_permutation_fuzz(secret, n):
    G = generate_graph(secret, n=n, p=0.5)
    perm = generate_random_permutation(G)
    nodes = sorted(G.nodes())
    # The permutation must be a rearrangement of the original nodes.
    assert sorted(perm) == nodes


# Fuzz test for applying isomorphism:
@given(
    secret=st.binary(min_size=1, max_size=32),
    n=st.integers(min_value=1, max_value=20),
    p=st.floats(min_value=0.0, max_value=1.0, allow_infinity=False, allow_nan=False),
)
def test_apply_isomorphism_fuzz(secret, n, p):
    G = generate_graph(secret, n=n, p=p)
    perm = generate_random_permutation(G)
    G_iso = apply_isomorphism(G, perm)
    # Ensure that the relabeled graph is isomorphic to the original.
    assert nx.is_isomorphic(G, G_iso)


# Fuzz test for the protocol:
@given(
    secret=st.binary(min_size=1, max_size=32),
    n=st.integers(min_value=3, max_value=20),
    p=st.floats(min_value=0.0, max_value=1.0, allow_infinity=False, allow_nan=False),
)
def test_protocol_fuzz(secret, n, p):
    G1 = generate_graph(secret, n=n, p=p)
    perm = generate_random_permutation(G1)
    G2 = apply_isomorphism(G1, perm)
    # Run a short protocol with 5 rounds.
    result = execute_protocol(G1, G2, perm, rounds=5)
    assert result is True


# Fuzz test for graph rotation:
@settings(deadline=None)  # Disable the deadline for this test.
@given(
    secret=st.binary(min_size=1, max_size=32),
    nonce=st.binary(min_size=1, max_size=16),
    n=st.integers(min_value=1, max_value=20),
    p=st.floats(min_value=0.0, max_value=1.0, allow_infinity=False, allow_nan=False),
)
def test_rotate_graph_fuzz(secret, nonce, n, p):
    new_G1, new_secret_iso = rotate_graph(secret, nonce, n=n, p=p)
    # Ensure the new graph has n nodes.
    assert new_G1.number_of_nodes() == n
    # Check that new_secret_iso is a valid permutation for new_G1.
    assert sorted(new_secret_iso) == sorted(new_G1.nodes())
