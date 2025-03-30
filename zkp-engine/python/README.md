# CheckMate ZKP Engine - Python Implementation

This folder contains the Python prototype for the CheckMate Zero-Knowledge Proof Engine. The implementation includes:

- **src/**
  - **graph.py:** Functions for graph generation and applying isomorphisms.
  - **commitment.py:** Functions for creating and verifying commitments.
  - **protocol.py:** Orchestrates the ZKP rounds (commitment, challenge, and response).
  - **rotation.py:** Handles secure rotation of graphs and isomorphisms.

- **tests/**
  - Unit tests for each module to ensure functionality and security.

Future implementations (e.g., in Rust) can be added in separate subfolders within the `zkp-engine` directory.
