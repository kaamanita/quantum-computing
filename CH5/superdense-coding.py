import pennylane as qml
from pennylane import numpy as np

dev = qml.device('default.qubit', wires=['A', 'B'], shots=500)

########################################

def prepare_bellstate():
    qml.Hadamard(wires='A')
    qml.CNOT(wires=['A', 'B'])

########################################

@qml.qnode(dev)
def superdense_coding(bit1, bit2):
    prepare_bellstate()

    # Sender
    qml.cond(bit2==1, qml.X)(wires='A')
    qml.cond(bit1==1, qml.Z)(wires='A')

    # Receiver
    qml.CNOT(wires=['A', 'B'])
    qml.Hadamard(wires='A')
    return qml.counts(wires=['A', 'B'])

########################################

def main():

    print('The sample counts for the decoded qubits are:')
    counts = superdense_coding(1, 0)
    # Expected result: {'10': 500}
    print(counts)


########################################

if __name__ == '__main__':
    main()
