"""
Module for graph rotation functions for the CheckMate ZKP Engine.
"""

from typing import List, Tuple

import networkx as nx
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

from .graph import generate_graph, generate_random_permutation


def rotate_graph(
    secret: bytes, nonce: bytes, n: int = 10, p: float = 0.3
) -> Tuple[nx.Graph, List[int]]:
    """
    Rotate the graph and secret isomorphism using a new nonce.

    This function derives a new shared secret from the original secret and a nonce,
    then generates a new graph and a new secret isomorphism (permutation) deterministically.

    :param secret: Original shared secret (bytes).
    :param nonce: A secure random nonce (bytes).
    :param n: Number of nodes for the new graph.
    :param p: Probability of edge creation for the new graph.
    :return: Tuple (new_G1, new_secret_iso).
    """
    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=16,  # Use a fixed length (e.g., 16 bytes) for the seed.
        salt=nonce,
        info=b"CheckMate graph rotation",
    )
    new_secret = hkdf.derive(secret)

    new_G1 = generate_graph(new_secret, n=n, p=p)
    new_seed = int.from_bytes(new_secret, byteorder="big")
    new_secret_iso = generate_random_permutation(new_G1, seed=new_seed)
    return new_G1, new_secret_iso
