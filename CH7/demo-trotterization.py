import pennylane as qml
from pennylane import numpy as np

mat = np.zeros((4, 4), dtype=np.complex128)            # Markov matrix
mat[0,0] = -7/25;                  mat[1,0] = 6 * np.sqrt(3) / 10
mat[2,1] = 6 * np.sqrt(3) / 10;    mat[1,1] = 2/4
mat[2,2] = 7/25;                   mat[3,2] = 8/10
mat[2,3] = 8/10;                   mat[1,3] = -2/4

########################################

dev = qml.device('default.qubit', wires=[0,1])

########################################

def make_hamiltonian(opr):
    hermitian = 0.5 * (opr + opr.T.conj())             # Enforce Hermitian matrix
    hamiltonian = qml.pauli_decompose(hermitian, wire_order=[0,1])
    return hamiltonian

@qml.qnode(dev, shots=1000)
def evolution_circuit():
    hmlt = make_hamiltonian(mat)
    qml.TrotterProduct(hmlt, time=10.0, n=20)          # Run for 10 steps with
                                                       # granularity degree n = 100
    return qml.counts(wires=[0,1])

########################################

def main():
    print('Sample counts for final states are:')
    counts = evolution_circuit()
    print(counts)
    # Expect result: {'00': 600, '01': 125, '10': 250, '11': 25}
    # These are probable final states after 10 steps of time evolution

########################################

if __name__ == '__main__':
    main()
