"""
Module for commitment functions used in the CheckMate ZKP Engine.
"""

import hashlib
import json
import secrets
from typing import List, Optional, Tuple


def commit_permutation(
    permutation: List, salt: Optional[bytes] = None
) -> Tuple[str, bytes]:
    """
    Create a cryptographic commitment for a permutation using SHA-256.

    :param permutation: The permutation list to commit to.
    :param salt: Optional salt (bytes). If not provided, a new salt is generated.
    :return: A tuple (commitment as hex string, salt used).
    """
    if salt is None:
        salt = secrets.token_bytes(16)
    perm_bytes = json.dumps(permutation, sort_keys=True).encode("utf-8")
    data = perm_bytes + salt
    commitment = hashlib.sha256(data).hexdigest()
    return commitment, salt


def verify_commitment(permutation: List, salt: bytes, commitment: str) -> bool:
    """
    Verify that a given commitment matches the permutation and salt.

    :param permutation: The permutation to verify.
    :param salt: The salt originally used.
    :param commitment: The expected commitment hex digest.
    :return: True if the commitment is valid, False otherwise.
    """
    perm_bytes = json.dumps(permutation, sort_keys=True).encode("utf-8")
    data = perm_bytes + salt
    expected_commitment = hashlib.sha256(data).hexdigest()
    return expected_commitment == commitment
