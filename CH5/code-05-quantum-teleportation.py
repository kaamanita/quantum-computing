############################################################
#
# Author: Prachya Boonkwan
# Affiliation: SIIT, Thammasat Univeristy
# License: CC-BY-NC 4.0
#
############################################################

import pennylane as qml
from pennylane import numpy as np

dev = qml.device('default.qubit', wires=['S', 'A', 'B'])

########################################

def prepare_bellstate():
    qml.Hadamard(wires='A')
    qml.CNOT(wires=['A', 'B'])

def sender(info):
    qml.cond(info==1, qml.X)(wires=['S'])
    qml.CNOT(wires=['S', 'A'])
    qml.Hadamard(wires='S')

def receiver(p, q):
    qml.cond(q, qml.X)(wires='B')
    qml.cond(p, qml.Z)(wires='B')

########################################

@qml.qnode(dev, shots=500)
def quantum_teleportation(info):
    prepare_bellstate()                              # Bell state |Phi+> as carrier
    sender(info)                                     # Encrypt the message
    (p, q) = (qml.measure('S'), qml.measure('A'))    # Measure (p,q) and send them
    receiver(p, q)                                   # via classical communication
    return qml.probs(wires='B')                      # Receiver extracts the message

########################################

def main():
    print('The teleported qubit is:')
    probs = quantum_teleportation(info=1)
    # Expected result: [0.0, 1.0]
    print(probs)

########################################

if __name__ == '__main__':
    main()
