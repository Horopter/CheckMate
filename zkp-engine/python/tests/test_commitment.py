from src.commitment import commit_permutation, verify_commitment

def test_commitment_and_verification():
    # Define a sample permutation.
    permutation = [3, 1, 4, 2, 0]
    commitment, salt = commit_permutation(permutation)
    # Verifying with the same permutation and salt must succeed.
    assert verify_commitment(
        permutation, salt, commitment
    ), "Commitment verification should pass with correct data."


def test_commitment_failure_on_modified_permutation():
    permutation = [0, 1, 2, 3, 4]
    commitment, salt = commit_permutation(permutation)
    # Modify the permutation.
    modified_permutation = permutation.copy()
    modified_permutation[0], modified_permutation[1] = (
        modified_permutation[1],
        modified_permutation[0],
    )
    # Verification must fail with a modified permutation.
    assert not verify_commitment(
        modified_permutation, salt, commitment
    ), "Modified permutation should not verify against original commitment."
