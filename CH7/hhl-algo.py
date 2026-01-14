import pennylane as qml
from pennylane import numpy as np

# Linear equation system:
#  2a + 3b - 4c + 5d = 70
# -3a +  b + 2c + 0d = 50
#   a + 2b + 3c +  d = 60
#  2a + 2b + 2c + 3d = 40
mat = np.array([ [ 2, 3, -4, 5],
                 [-3, 1,  2, 0],
                 [ 1, 2,  3, 1],
                 [ 2, 2,  2, 3] ], dtype=np.complex128)
bvec = np.array([70, 50, 60, 40], dtype=np.complex128)

########################################

extra_wires = ['x']
target_wires = ['t0','t1']
estimation_wires = ['e1','e2','e3','e4','e5']
check_wires = ['f']

dev = qml.device('default.qubit',
                 wires=extra_wires + target_wires + estimation_wires + check_wires)

########################################

def normalize_les(mat, bvec):
    norm_a = np.max(np.linalg.svd(mat)[1])
    norm_b = np.linalg.norm(bvec)
    return mat / norm_a, bvec / norm_b

########################################

@qml.qnode(dev, shots=1000)
def hhl_circuit(mat, bvec):
    mat, bvec = normalize_les(mat, bvec)                # Normalize A and b
    qml.AmplitudeEmbedding(bvec, wires=target_wires)    # Initialize the circuit with b
    qml.QuantumPhaseEstimation(                         # Extract eigenvalues with block encoding
        qml.BlockEncode(mat, wires=extra_wires + target_wires),
        estimation_wires=estimation_wires               # We need an extra qubit for block encoding
    )
    qml.ControlledSequence(                             # Compute the filter flag and the
        qml.Y(wires=check_wires),                       # inverse of eigenvalues
        control=estimation_wires
    )
    qml.adjoint(qml.QuantumPhaseEstimation)(            # Clean up the qubitization
        qml.BlockEncode(mat, wires=extra_wires + target_wires),
        estimation_wires=estimation_wires
    )
    m = qml.measure(wires=check_wires, postselect=1)    # Redo if the check flag is 0
    return qml.probs(wires=target_wires)

########################################

def main():
    print('The solution [x1, x2, x3, x4] of LES is:')
    probs = hhl_circuit(mat, bvec)
    print(probs)
    # Solution is a unit vector for each variable
    # Result: [0.0, 0.40, 0.25, 0.35 ]  ->  a = 0, b = 0.4, c = 0.25, d = 0.35

########################################

if __name__ == '__main__':
    main()
