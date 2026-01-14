import pennylane as qml
from pennylane import numpy as np

secret_code = [0,1,0,0,1,1,0,1]
no_bits = len(secret_code)
dev = qml.device('default.qubit', wires=no_bits + 1)

########################################

def oracle(secret_code, wires):

    for i in range(len(secret_code)):              # CCX for each bit of the oracle
        if secret_code[i] == 1:
            qml.CNOT(wires=[wires[i], wires[-1]])

########################################

@qml.qnode(dev, shots=500)
def bernstein_vazirani(secret_code):

    qml.X(wires=no_bits)                           # Prepare state |+>^N (*) |-> from |0>^(N+1)
    qml.Hadamard(wires=no_bits)
    for i in range(no_bits):
        qml.Hadamard(wires=[i])
    oracle(secret_code, range(no_bits + 1))        # Apply the oracle operator U_f
    for i in range(no_bits):                       # Extract the oracle from qubits[1:N]
        qml.Hadamard(wires=[i])
    return qml.counts(wires=range(no_bits))        # Return the oracle

########################################

def main():
    print(f'Secret code: {secret_code}')
    counts = bernstein_vazirani(secret_code)
    print('The sample counts for secret code guess are:')
    print(counts)

########################################

if __name__ == '__main__':
    main()
