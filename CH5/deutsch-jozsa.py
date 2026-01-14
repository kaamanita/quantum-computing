import pennylane as qml
from pennylane import numpy as np

no_bits = 4                                    # Length of the hash code
dev = qml.device('default.qubit', wires=no_bits + 1, shots=500)

########################################

def oracle(theta1, theta2, theta3):

    # Compute a hash code from the input wires
    qml.RX(theta1, wires=[0]);    qml.CNOT(wires=[0, 1])
    qml.RZ(theta2, wires=[2]);    qml.CNOT(wires=[2, 3])
    qml.RY(theta3, wires=4)
    qml.Toffoli(wires=[0, 2, no_bits])         # Last bit is the type of this hash code

########################################

@qml.qnode(dev)
def deutsch_jozsa():

    qml.X(wires=no_bits)                       # Prepare state |+>^N (*) |-> from |0>^(N+1)
    qml.Hadamard(wires=no_bits)
    for i in range(no_bits):
        qml.Hadamard(wires=[i])
    oracle(np.pi / 4, np.pi / 4, np.pi / 4)    # Apply the oracle operator U_f
    for i in range(no_bits):                   # Extract the balance from the last qubit
        qml.Hadamard(wires=[i])
    return qml.probs(wires=[no_bits])          # Return the balance

########################################

def main():

    print('The balance of oracle U_f is:')
    probs = deutsch_jozsa()
    # Expected result: [0.65, 0.35]
    print(probs)

########################################

if __name__ == '__main__':
    main()
