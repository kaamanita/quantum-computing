############################################################
#
# Author: Prachya Boonkwan
# Affiliation: SIIT, Thammasat Univeristy
# License: CC-BY-NC 4.0
#
############################################################

import pennylane as qml
from pennylane import numpy as np

dev = qml.device('default.qubit', wires=['S1', 'S2', 'X1', 'X2', 'X3', 'X4'])

########################################

def prepare_bellstate(wire1, wire2, minus=False):
    qml.Hadamard(wires=wire1)
    if minus:
        qml.PauliX(wires=wire2)
    qml.CNOT(wires=[wire1, wire2])

def prepare_chistate(wire1, wire2, wire3, wire4):
    prepare_bellstate(wire1, wire2, minus=False)
    prepare_bellstate(wire3, wire4, minus=False)
    qml.CNOT(wires=[wire3, wire2])

def sender(input1, input2, x1, x2, x3, x4):
    qml.CNOT(wires=[input1, x1])
    qml.CNOT(wires=[x4, input2])
    qml.Hadamard(wires=input1)
    qml.Hadamard(wires=x4)

def receiver(p1, q1, p2, q2, x2, x3):
    qml.cond(p1, qml.Z)(wires=x2)
    qml.cond(p1, qml.Z)(wires=x3)
    qml.cond(p2, qml.X)(wires=x2)
    qml.cond(p2, qml.X)(wires=x3)
    qml.cond(q1, qml.X)(wires=x2)
    qml.cond(q2, qml.Z)(wires=x3)
    qml.CNOT(wires=[x3, x2])

########################################
    
@qml.qnode(dev, shots=500)
def quantum_gate_teleportation(info):
    prepare_bellstate('S1', 'S2', minus=info)     # Input entangled state
    prepare_chistate('X1', 'X2', 'X3', 'X4')      # Prepare the chi state
    sender('S1', 'S2', 'X1', 'X2', 'X3', 'X4')    # Sender part
    p1 = qml.measure('S1')                        # Measure four qubits
    p2 = qml.measure('S2')
    q1 = qml.measure('X1')
    q2 = qml.measure('X4')
    receiver(p1, p2, q1, q2, 'X2', 'X3')          # Receiver part
    return qml.counts(wires=['X2', 'X3'])

########################################

def main():

    print('The sample counts of teleported qubits are:')
    counts = quantum_gate_teleportation(info=True)             # False = Bell-plus, True = Bell-minus
    # Expected result: {'01': 250, '10': 250}
    print(counts)

########################################

if __name__ == '__main__':
    main()
