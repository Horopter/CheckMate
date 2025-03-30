# CheckMate ZKP Engine Design Document

## 1. Overview

The CheckMate ZKP Engine is the cryptographic core of the CheckMate application. Its primary purpose is to implement a graph isomorphism-based zero-knowledge proof (ZKP) protocol, enabling mutual authentication between two devices. This prototype is initially implemented in Python, with a planned pivot to Rust for performance and safety in future iterations.

## 2. Scope and Objectives

- **Primary Goal:**  
  Provide a robust ZKP mechanism based on graph isomorphism to verify the authenticity of users during a call, preventing impersonation via deepfakes or AI voice cloning.

- **Objectives:**
  - Implement a GMW-style protocol where each party proves knowledge of an isomorphism between two graphs.
  - Generate graphs from a shared secret, ensuring reproducibility.
  - Support multiple rounds (e.g., 10 rounds) to reduce the cheating probability to \( \frac{1}{1024} \).
  - Include a graph rotation mechanism using a shared secret-derived seed and nonce to maintain unlinkability.
  - Ensure cryptographic operations use secure randomness and proper key management.

## 3. Cryptographic Protocol: Graph Isomorphism ZKP

### 3.1 Protocol Overview

The protocol uses two graphs:
- **\( G_1 \):** Generated from a shared secret using a key derivation function (KDF).
- **\( G_2 \):** A permutation (isomorphic copy) of \( G_1 \) using a secret isomorphism \( \pi \).

The ZKP process follows these steps for each round:
1. **Commitment:**  
   - The prover selects a random permutation \( \sigma \) of \( G_1 \) and computes a commitment to the permuted graph.
2. **Challenge:**  
   - The verifier sends a challenge bit (0 or 1).
3. **Response:**  
   - Depending on the challenge:
     - If the challenge is 0, the prover reveals the random permutation \( \sigma \).
     - If the challenge is 1, the prover reveals the composition \( \pi \circ \sigma \).
4. **Verification:**  
   - The verifier checks that the response corresponds correctly with the initial commitment and the known graph \( G_2 \) (if applicable).

Repeating this process for 10 rounds reduces the probability of a cheating prover succeeding to \( \frac{1}{1024} \).

### 3.2 Graph Generation and Rotation

- **Graph Generation:**  
  - \( G_1 \) is generated deterministically from a shared secret using a KDF (e.g., HKDF) to derive a seed for a pseudo-random graph generator.
- **Graph Rotation:**  
  - On compromise or after a set period, both the graph and the secret isomorphism \( \pi \) are rotated.  
  - A secure random nonce combined with the shared secret (via a KDF) is used to generate new values, ensuring that successive graphs are unlinkable.

## 4. Design Architecture

### 4.1 Modular Components

- **Graph Module:**  
  - **Purpose:** Generate \( G_1 \) using a shared secret and create \( G_2 \) via a secret isomorphism \( \pi \).
  - **Functions:**  
    - `generate_graph(secret: bytes) -> Graph`
    - `apply_isomorphism(graph: Graph, isomorphism: Permutation) -> Graph`

- **Commitment Module:**  
  - **Purpose:** Manage commitments and responses during the ZKP rounds.
  - **Functions:**  
    - `commit_permutation(graph: Graph, permutation: Permutation) -> Commitment`
    - `verify_commitment(commitment: Commitment, response: Response, challenge: int) -> bool`

- **Protocol Controller:**  
  - **Purpose:** Orchestrate the rounds of the ZKP protocol.
  - **Functions:**  
    - `run_round(prover_state, verifier_state) -> bool`
    - `execute_protocol(rounds: int = 10) -> bool`

- **Rotation Module:**  
  - **Purpose:** Rotate graphs and isomorphisms securely.
  - **Functions:**  
    - `rotate_graph(secret: bytes, nonce: bytes) -> (Graph, Permutation)`

### 4.2 Data Flow and Interfaces

1. **Initialization:**  
   - Both parties derive \( G_1 \) from the shared secret.
   - One party generates \( G_2 \) by applying the secret isomorphism \( \pi \).

2. **ZKP Rounds:**  
   - The prover commits to a permuted version of \( G_1 \) using a random permutation.
   - The verifier sends a challenge bit.
   - The prover sends back a response based on the challenge.
   - The verifier checks the response against the commitment.

3. **Graph Rotation:**  
   - When triggered, both parties use the rotation module to generate a new \( G_1 \) and \( \pi \), using a new nonce.

## 5. Implementation Details (Python Prototype)

### 5.1 Library Choices

- **Graph Handling:**  
  - Consider using `networkx` for graph generation and manipulation.
- **Cryptographic Functions:**  
  - Python’s built-in `secrets` module for secure randomness.
  - `hashlib` and `hmac` for hashing and commitment schemes.
  - Use `cryptography` library for key derivation (HKDF) if needed.

### 5.2 Code Structure

- **Directory Layout:**  
zkp-engine/ 
├── src/ 
│ ├── init.py 
│ ├── graph.py # Graph generation and isomorphism functions 
│ ├── commitment.py # Commitment and verification logic 
│ ├── protocol.py # ZKP protocol orchestration 
│ └── rotation.py # Graph rotation functions 
├── tests/ 
│ ├── test_graph.py 
│ ├── test_commitment.py 
│ ├── test_protocol.py 
│ └── test_rotation.py 
└── README.md


### 5.3 Example Pseudocode

Below is a simplified pseudocode snippet illustrating a single round of the protocol:

```python
def run_zkp_round(G1, G2, secret_iso):
  # Prover: generate a random permutation σ and compute the commitment
  sigma = generate_random_permutation(G1)
  commitment = commit_permutation(G1, sigma)
  
  # Verifier: generate a random challenge bit (0 or 1)
  challenge = secrets.randbits(1)
  
  # Prover: based on the challenge, compute the response
  if challenge == 0:
      response = sigma
  else:
      response = compose(secret_iso, sigma)  # π ∘ σ
  
  # Verifier: verify the response against the commitment
  valid = verify_commitment(commitment, response, challenge, G1, G2)
  return valid
```

# Security, Testing, Future Work, and Conclusion

## 6. Security Considerations

- **Randomness:**  
  Use Python's `secrets` module for all random number generation to ensure cryptographic security.
- **Key Derivation and Graph Generation:**  
  Use HKDF or a similar KDF to derive seeds from shared secrets.
- **Commitment Integrity:**  
  Ensure that commitments are collision-resistant and binding.
- **Rotation and Unlinkability:**  
  Graph rotations must be executed in a way that prevents linking previous sessions with new ones.

## 7. Testing and Validation

- **Unit Tests:**  
  Write tests for each module (graph generation, commitment verification, rotation, etc.).
- **Integration Tests:**  
  Simulate complete protocol runs to verify that the ZKP process is sound and secure.
- **Adversarial Scenarios:**  
  Test against replay attacks, MITM attempts, and incorrect challenge responses to ensure robustness.

## 8. Future Work and Enhancements

- **Migration to Rust:**  
  Once the Python prototype is validated, plan to migrate the engine to Rust for enhanced performance and memory safety.
- **Enhanced Protocols:**  
  Explore integrating additional biometric or fallback mechanisms.
- **Security Audits:**  
  Schedule external security audits after finalizing the core protocol.
- **API & SDK Development:**  
  Develop clear APIs for seamless integration with the mobile app and relay server.

## 9. Conclusion

This document outlines the security considerations, testing strategies, and future enhancements for the CheckMate ZKP Engine. Implementing rigorous testing and validation, combined with plans for future upgrades, will ensure that the engine meets the required security and performance benchmarks. Future work will focus on refining the protocol, enhancing overall security, and preparing for full integration with the CheckMate system.
