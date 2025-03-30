import time

import networkx as nx
import pytest

from src.commitment import commit_permutation, verify_commitment
# Import functions from our modules (thanks to conftest.py adding "src" to PYTHONPATH)
from src.graph import (apply_isomorphism, generate_graph,
                   generate_random_permutation)
from src.protocol import execute_protocol, run_zkp_round
from src.rotation import rotate_graph


# ------------------------------------------------------------------
# 1. Test that different secrets yield different graphs (edge sets differ)
def test_different_secrets_generate_different_graphs():
    secret1 = b"secret1"
    secret2 = b"secret2"
    n = 10
    p = 0.5
    G1 = generate_graph(secret1, n=n, p=p)
    G2 = generate_graph(secret2, n=n, p=p)
    # Even if two graphs are abstractly isomorphic, the actual edge sets should differ.
    edges1 = sorted(G1.edges())
    edges2 = sorted(G2.edges())
    assert (
        edges1 != edges2
    ), "Graphs generated with different secrets should differ in edge sets."


# ------------------------------------------------------------------
# 2. Test tampered commitment: modifying the permutation should fail verification.
def test_tampered_commitment():
    permutation = [1, 2, 3, 4, 0]
    commitment, salt = commit_permutation(permutation)
    # Tamper with the permutation (swap two elements)
    tampered_permutation = permutation.copy()
    tampered_permutation[0], tampered_permutation[1] = (
        tampered_permutation[1],
        tampered_permutation[0],
    )
    assert not verify_commitment(
        tampered_permutation, salt, commitment
    ), "Tampered permutation should fail commitment verification."


# ------------------------------------------------------------------
# 3. Test tampered protocol response:
def test_tampered_response_protocol():
    secret = b"protocol_tamper"
    n = 10
    p = 0.5
    G1 = generate_graph(secret, n=n, p=p)
    secret_iso = generate_random_permutation(G1)
    G2 = apply_isomorphism(G1, secret_iso)
    valid, challenge, response, commitment, salt = run_zkp_round(G1, G2, secret_iso)
    # Tamper with the response by altering its first element
    tampered_response = response.copy()
    tampered_response[0] = (tampered_response[0] + 1) % n
    # Depending on the challenge, verify accordingly:
    if challenge == 0:
        tampered_valid = verify_commitment(tampered_response, salt, commitment)
    else:
        tampered_graph = apply_isomorphism(G1, tampered_response)
        tampered_valid = nx.is_isomorphic(tampered_graph, G2)
    assert not tampered_valid, "Tampered response should not verify correctly."


# ------------------------------------------------------------------
# 4. Test protocol under a large number of rounds (load test)
def test_large_number_of_rounds_protocol():
    secret = b"protocol_large"
    n = 10
    p = 0.5
    G1 = generate_graph(secret, n=n, p=p)
    secret_iso = generate_random_permutation(G1)
    G2 = apply_isomorphism(G1, secret_iso)
    rounds = 50  # Increase this number for heavier load if desired
    start = time.time()
    result = execute_protocol(G1, G2, secret_iso, rounds=rounds)
    duration = time.time() - start
    assert result, f"Protocol should succeed for {rounds} rounds."
    # Optional: enforce that protocol runs reasonably fast (e.g., under 2 seconds)
    assert (
        duration < 2
    ), f"Protocol took too long ({duration:.2f} seconds) for {rounds} rounds."


# ------------------------------------------------------------------
# 5. Test randomness: without seed, multiple calls should produce different permutations
def test_random_permutation_without_seed_variability():
    secret = b"random_test"
    G = generate_graph(secret, n=10, p=0.5)
    perm1 = generate_random_permutation(G)
    perm2 = generate_random_permutation(G)
    # They should not be identical most of the time.
    assert (
        perm1 != perm2
    ), "Random permutations without seed should differ most of the time."


# ------------------------------------------------------------------
# 6. Test that an empty secret (or very short secret) still functions (or raises an error as desired)
def test_empty_secret_behavior():
    # You might want to enforce a minimum secret length.
    # For this test, we check that an empty secret still produces a graph.
    secret = b""
    n = 5
    p = 0.5
    try:
        G = generate_graph(secret, n=n, p=p)
    except Exception:
        pytest.skip("Empty secret not supported, skipping test.")
    else:
        assert (
            G.number_of_nodes() == n
        ), "Graph generated from empty secret should have the correct number of nodes."


# ------------------------------------------------------------------
# 7. Test rotation with different nonces yields different isomorphisms
def test_rotation_different_nonces():
    secret = b"rotate_secret_test"
    nonce_a = b"nonce_a"
    nonce_b = b"nonce_b"
    n = 10
    p = 0.5
    new_G1_a, new_secret_iso_a = rotate_graph(secret, nonce_a, n=n, p=p)
    new_G1_b, new_secret_iso_b = rotate_graph(secret, nonce_b, n=n, p=p)
    # Even if the graphs may be isomorphic, the secret isomorphisms should differ.
    assert (
        new_secret_iso_a != new_secret_iso_b
    ), "Different nonces should yield different secret isomorphisms."
