import pennylane as qml
from pennylane import numpy as np

# A unitary matrix
mat = np.zeros((4, 4), dtype=np.complex128)
mat[0,0] = -7/25;                  mat[1,0] = 6 * np.sqrt(3) / 10
mat[2,1] = 6 * np.sqrt(3) / 10;    mat[1,1] = 2/4
mat[2,2] = 7/25;                   mat[3,2] = 8/10
mat[2,3] = 8/10;                   mat[1,3] = -2/4

########################################

target_wires = ['t0','t1']                            # N = input qubits
control_wires = ['c1','c2','c3','c4']                 # 2^N wires
estimation_wires = ['e1','e2','e3','e4','e5','e6']    # Granularity

dev = qml.device('default.qubit', wires=target_wires + control_wires + estimation_wires)

########################################

def make_hamiltonian(opr):
    hermitian = 0.5 * (opr + opr.T.conj())
    hamiltonian = qml.pauli_decompose(hermitian, wire_order=target_wires)
    return hamiltonian

########################################

@qml.qnode(dev)
def evolution_circuit(hmlt):
    qml.QuantumPhaseEstimation(
        qml.Qubitization(hmlt, control_wires),
        estimation_wires=estimation_wires
    )
    return qml.probs(wires=estimation_wires)

########################################

def main():
    print('Original matrix is:')
    print(mat)
    hmlt = make_hamiltonian(mat)    # Convert a unitary matrix to a Hamiltonian
    normconst = sum([abs(coeff) for coeff in hmlt.terms()[0]])    # Normalizing constant

    print('\nIts Hamiltonian is:')
    print(qml.matrix(hmlt).real)    # This is how we print a Hamiltonian out in the matrix form

    print('\nWe extract its information:')
    probs = evolution_circuit(hmlt)
    r = np.argmax(probs)
    phase = 2 * np.pi * r / 2 ** len(estimation_wires)
    eigval = np.cos(phase) * normconst
    print(f'phase = {phase}')
    print(f'eigenvalue = {eigval}')
    # Expected result:
    # phase = 1.7671
    # eigenvalue = -0.4096

########################################

if __name__ == '__main__':
    main()
