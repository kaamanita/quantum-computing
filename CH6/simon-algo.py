import pennylane as qml
from pennylane import numpy as np

no_qubits = 4
wires = range(2 * no_qubits)
input_wires, output_wires = wires[0 : no_qubits], wires[no_qubits : 2*no_qubits]
dev = qml.device('default.qubit', wires=wires)

########################################

def f_mto1(input_wires, output_wires):                   # Black box function (many to one)

    qml.CNOT(wires=[input_wires[3], output_wires[0]])    # Input:  |x0, x1, x2, x3>
    qml.CNOT(wires=[input_wires[1], output_wires[1]])    # Output: |x3, x1, x0 && x1, x1 && x2>
    qml.Toffoli(wires=[input_wires[0], input_wires[1], output_wires[2]])
    qml.Toffoli(wires=[input_wires[1], input_wires[2], output_wires[3]])

########################################

@qml.qnode(device=dev, shots=1000)
def simon_algo():                                        # Simon's algorithm

    for i in input_wires:
        qml.Hadamard(wires=i)
    f_mto1(input_wires, output_wires)
    for i in input_wires:
        qml.Hadamard(wires=i)
    return qml.counts(wires=output_wires)

########################################

def main():

    print('The balance of this oracle function is:')
    counts = simon_algo()
    # Expected result: {'0000': 250, '0100': 62.5, '0101': 62.5, '0110': 62.5, '0111': 62.5,
    #                   '1000': 250, '1100': 62.5, '1101': 62.5, '1110': 62.5, '1111': 62.5}
    print(counts)

########################################

if __name__ == '__main__':
    main()
