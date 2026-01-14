import pennylane as qml
from pennylane import numpy as np

basis_wires = ['d1', 'd2', 'd3']
angular_wires = ['g1', 'g2', 'g3']
amplitude_wires = ['a1', 'a2', 'a3']

dev = qml.device('default.qubit', wires=basis_wires + angular_wires + amplitude_wires)

########################################

@qml.qnode(dev, shots=100)
def embedding_circuit():
    # Basis encoding: N binary digits -> N qubits
    bitstring = [1, 0, 1]
    qml.BasisEmbedding(features=bitstring, wires=basis_wires)
    # Angular encoding: N continuous values -> N qubits
    angles = [np.pi / 4, np.pi / 3, np.pi / 2]
    qml.AngleEmbedding(features=angles, wires=angular_wires)
    # Amplitude encoding: 2^N continuous values -> N qubits
    amplitudes = [2.0, 1.0, 3.0, 7.0, 5.0, 4.0, 8.0, 6.0]
    amplitudes = amplitudes / np.linalg.norm(amplitudes)        # Normalization is required
    qml.AmplitudeEmbedding(features=amplitudes, wires=amplitude_wires)
    # Measurements
    return ( qml.counts(wires=basis_wires),
             qml.counts(wires=angular_wires),
             qml.counts(wires=amplitude_wires) )

########################################

def main():
    basis_counts, angular_counts, amplitude_counts = embedding_circuit()
    print('Sample counts of basis encoding:')
    print(basis_counts)
    print('\nSample counts of angular encoding:')
    print(angular_counts)
    print('\nSample counts of amplitude encoding:')
    print(amplitude_counts)

########################################

if __name__ == '__main__':
    main()
