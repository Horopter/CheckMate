"""
Module for graph generation and isomorphism functions for the CheckMate ZKP Engine.
"""

from typing import List, Optional

import networkx as nx
import numpy as np
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import secrets

def derive_seed(secret: bytes, length: int = 16) -> int:
    """
    Derive an integer seed from a shared secret using HKDF.
    """
    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=length,
        salt=None,
        info=b"CheckMate graph generation",
    )
    key_material = hkdf.derive(secret)
    seed = int.from_bytes(key_material, byteorder="big")
    return seed


def generate_graph(secret: bytes, n: int = 10, p: float = 0.3) -> nx.Graph:
    """
    Generate a random Erdos-Renyi graph deterministically from a shared secret.

    Validates parameters:
      - n must be non-negative.
      - p must be between 0 and 1 (inclusive).

    :param secret: Shared secret (bytes).
    :param n: Number of nodes.
    :param p: Probability for edge creation.
    :return: Generated NetworkX graph.
    :raises ValueError: If n < 0 or if p is not in [0,1].
    """
    if n < 0:
        raise ValueError("Number of nodes must be non-negative")
    if not (0 <= p <= 1):
        raise ValueError("Edge probability must be between 0 and 1")

    seed = derive_seed(secret)
    rng = np.random.default_rng(seed)
    nx_seed = int(rng.integers(0, 2**32))
    graph_obj = nx.erdos_renyi_graph(n, p, seed=nx_seed)
    return graph_obj


def deterministic_shuffle(lst: List, seed: int) -> List:
    """
    Deterministically shuffle a list using AES in CTR mode.
    
    This function uses a cryptographic block cipher (AES) in CTR mode to generate
    a pseudorandom byte stream from a given seed. That byte stream is then used
    to perform a Fisher–Yates shuffle. This approach is both cryptographically secure
    and deterministic when a seed is provided.
    
    :param lst: List to shuffle.
    :param seed: An integer seed used to derive the AES key.
    :return: Shuffled list.
    """
    # Derive a 16-byte key from the seed.
    key = seed.to_bytes(16, byteorder="big", signed=False)
    # Use a fixed IV for determinism.
    iv = b"\x00" * 16
    cipher = Cipher(algorithms.AES(key), modes.CTR(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    arr = lst.copy()
    n = len(arr)
    for i in range(n - 1, 0, -1):
        # Generate 4 random bytes and convert to an integer.
        rand_bytes = encryptor.update(b"\x00" * 4)
        rand_int = int.from_bytes(rand_bytes, byteorder="big")
        j = rand_int % (i + 1)
        arr[i], arr[j] = arr[j], arr[i]
    return arr

def generate_random_permutation(graph: nx.Graph, seed: Optional[int] = None) -> List:
    """
    Generate a random permutation of the graph's node labels.
    If a seed is provided, the permutation will be deterministic using AES in CTR mode.
    
    :param graph: Input graph.
    :param seed: Optional integer seed for deterministic shuffling.
    :return: A permutation list.
    """
    nodes = sorted(graph.nodes())
    if seed is None:
        # Use cryptographically secure shuffling.
        permutation = nodes.copy()
        secrets.SystemRandom().shuffle(permutation)
        return permutation
    else:
        return deterministic_shuffle(nodes, seed)

def apply_isomorphism(graph: nx.Graph, permutation: List) -> nx.Graph:
    """
    Apply an isomorphism to a graph given a permutation.
    The permutation list maps sorted original nodes to new labels.

    :param graph: Input graph.
    :param permutation: Permutation list representing the isomorphism.
    :return: A new graph with nodes relabeled according to the permutation.
    """
    mapping = {node: permutation[i] for i, node in enumerate(sorted(graph.nodes()))}
    graph_iso = nx.relabel_nodes(graph, mapping)
    return graph_iso
