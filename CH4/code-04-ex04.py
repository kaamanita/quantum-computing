import pennylane as qml
from pennylane import numpy as np

dev = qml.device('default.qubit', wires=[0, 1, 2], shots=500)

########################################

@qml.qnode(dev)
def circuit(theta: float):

    qml.Hadamard(wires=[0])
    qml.CNOT(wires=[0, 1])         # Bell state |Psi+>
    qml.RX(theta, wires=[1])       # X-rotate wire-1 by theta

    # Postselection: If wire-1 is not 1, terminate this circuit run
    m = qml.measure(wires=[1], postselect=1)

    qml.cond(theta > np.pi / 2,    # If theta > pi / 2:
        true_fn=qml.RX,            #     X-rotate wire-2 by theta
        false_fn=qml.RY            # Else: Y-rotate wire-2 by theta
    )(theta, wires=[2])            # (Common parameters)

    return qml.counts()

########################################

def main():
    
    print('The sample counts for output states [000, ..., 111] are:')
    # Result: {'010': 40, '011': 10, '110': 150, '111': 50}.
    # N.B. It does not sum to 500 due to the postselection.
    print(circuit(np.pi / 3))

########################################

if __name__ == '__main__':
    main()
