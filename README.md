# Quantum Computing

This repository is dedicated for my course of Quantum Computing at SIIT, Thammasat University.

## Course Description

This course provides a comprehensive introduction to quantum computing, bridging the gap between theoretical physics and practical engineering applications. Starting with the mathematical foundations of complex linear algebra, students will progress through the core principles of qubits, quantum logic gates, and circuit design. The curriculum covers essential quantum algorithms (including Shor’s, Grover’s, and HHL), error correction, and system dynamics. A significant portion of the course is dedicated to the emerging fields of Quantum Machine Learning (QML) and variational algorithms (VQE, QAOA). Through the sessions, students will gain hands-on experience simulating quantum circuits and algorithms using the PennyLane framework, preparing them to tackle problems in cryptography, optimization, and system simulation on Noisy Intermediate-Scale Quantum (NISQ) devices.

## Format

There are 15 sessions (2 hours of lecture + up to 1 hour of Q&A).

1. **Introduction & Complex Numbers (CH1):**
   Complex numbers, polar forms, wave representation, inner/outer products, phase synchronicity.
    
2. **Complex Matrices (CH1):**
   Hermitian and Unitary matrices, eigen-decomposition, matrix exponentials, Householder reflection.
    
3. **Qubits, Operators, & Bloch Sphere (CH2):**
   Probability distributions, Dirac notation, Bloch sphere visualization, Universal rotation, global phase vs. relative phase.

4. **Quantum Logic & Entanglement (CH2):**
   Tensor products, multi-qubit systems, entanglement (Bell/GHZ/W-states), measurement bases.

5. **Circuit Design & PennyLane Basics (CH3):**
   The Clifford Set (Levels 1-3), constructing circuits in PennyLane, QNode decorators, state preparation algorithms.
    
6. **Measurement & Dynamic Circuits (CH4):**
   Analytical vs. Projective measurement, expectation values, variance. Introduction to dynamic circuits (loops, conditionals).

7. **Non-Clifford Gates & Noise (CH4):**
   Toffoli gates, generalized rotation, density matrices, mixed states, and simulating noise/decoherence.

8. **Foundational Algorithms (CH5):**
   Oracle separation, Phase Kickback technique. Bernstein-Vazirani and Deutsch-Jozsa algorithms.
    
9. **Communication & Error Correction (CH5):**
   No-Cloning theorem, Teleportation, Superdense coding. Quantum Error Correction (Repetition codes, Shor code).

10. **Grover’s Search Algorithm & QFT (CH6):**
    Unstructured search, amplitude amplification, geometric interpretation, optimal iteration counts, Quantum Fourier Transform (QFT), Inverse QFT.
    
11. **QPE & Cryptography (CH6):**
    Quantum Phase Estimation (QPE), logic behind Shor’s Algorithm and RSA breaking.
    
12. **System Dynamics & Automata (CH7):**
    Deterministic vs. Probabilistic vs. Quantum Finite-State Automata (QFA), Szegedy’s algorithm, Quantum Walks.

13. **Advanced Simulation (CH7):**
    Hamiltonian simulation, Trotter-Suzuki decomposition, HHL algorithm for linear systems, Quantum Signal Processing (QSP).
    
14. **Quantum Machine Learning (CH8):**
    Variational Quantum Algorithms (VQA), Ansatz design (HEA, TEN, ALT), Quantum Neural Networks (QNN), gradients (Parameter Shift Rule).
    
15. **Optimization & VQE (CH9):**
    Variational Quantum Eigensolver (VQE), QAOA for graph problems (Max-Cut, Max-Clique, Traveling Salesman Problem).

## Tools
    
Python, PennyLane, Generative AI

## License

All materials herein are under the CC-BY-NC 4.0 license.
