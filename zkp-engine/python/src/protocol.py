"""
Module for the ZKP protocol orchestration for the CheckMate ZKP Engine.
"""

import secrets
from typing import List, Tuple

import networkx as nx

from .commitment import commit_permutation, verify_commitment
from .graph import apply_isomorphism, generate_random_permutation


def run_zkp_round(
    G1: nx.Graph, G2: nx.Graph, secret_iso: List[int]
) -> Tuple[bool, int, List[int], str, bytes]:
    """
    Execute one round of the graph isomorphism ZKP protocol.

    Steps:
      1. Prover generates a random permutation (sigma) of G1 and commits to it.
      2. Verifier issues a random challenge bit (0 or 1).
      3. Prover responds:
         - If challenge is 0: sends sigma.
         - If challenge is 1: sends composition (secret_iso ∘ sigma).
      4. Verifier checks the commitment or that applying the response to G1 yields G2.

    :param G1: Original graph.
    :param G2: Isomorphic graph (i.e. applying secret_iso to G1 yields G2).
    :param secret_iso: Secret isomorphism as a permutation list.
    :return: Tuple (valid, challenge, response, commitment, salt).
    """
    # Prover: Generate a random permutation sigma and commit.
    sigma: List[int] = generate_random_permutation(G1)
    commitment, salt = commit_permutation(sigma)

    # Verifier: Generate a random challenge bit (0 or 1).
    challenge: int = secrets.randbits(1)

    # Prover: Compute response based on the challenge.
    if challenge == 0:
        response: List[int] = sigma
    else:
        response = [secret_iso[sigma[i]] for i in range(len(sigma))]

    # Verifier: Check the response.
    if challenge == 0:
        valid = verify_commitment(sigma, salt, commitment)
    else:
        G_prime = apply_isomorphism(G1, response)
        valid = nx.is_isomorphic(G_prime, G2)

    return valid, challenge, response, commitment, salt


def execute_protocol(
    G1: nx.Graph, G2: nx.Graph, secret_iso: List[int], rounds: int = 10
) -> bool:
    """
    Execute the ZKP protocol over multiple rounds.

    The protocol is considered successful only if all rounds validate correctly.

    :param G1: Original graph.
    :param G2: Graph obtained by applying the secret isomorphism to G1.
    :param secret_iso: Secret isomorphism as a permutation list.
    :param rounds: Number of rounds to execute (default 10).
    :return: True if all rounds are valid; False otherwise.
    """
    for _ in range(rounds):
        valid, challenge, response, commitment, salt = run_zkp_round(G1, G2, secret_iso)
        if not valid:
            return False
    return True
