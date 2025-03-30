from src.graph import (apply_isomorphism, generate_graph,
                   generate_random_permutation)
from src.protocol import execute_protocol, run_zkp_round


def test_single_round_protocol():
    secret = b"protocol_secret"
    n = 10
    p = 0.5
    G1 = generate_graph(secret, n=n, p=p)
    secret_iso = generate_random_permutation(G1)
    G2 = apply_isomorphism(G1, secret_iso)

    valid, challenge, response, commitment, salt = run_zkp_round(G1, G2, secret_iso)
    # In a correct protocol round, the response must be valid.
    assert valid, f"ZKP round failed (challenge {challenge}, response {response})."


def test_execute_protocol():
    secret = b"protocol_execute"
    n = 10
    p = 0.5
    G1 = generate_graph(secret, n=n, p=p)
    secret_iso = generate_random_permutation(G1)
    G2 = apply_isomorphism(G1, secret_iso)
    rounds = 10
    result = execute_protocol(G1, G2, secret_iso, rounds=rounds)
    assert result, "Executing protocol for multiple rounds should succeed."
