import pennylane as qml
from pennylane import numpy as np

dev = qml.device('default.qubit', wires=[0, 1, 2])

########################################

@qml.qnode(dev, shots=500)
def circuit(theta: float):
    qml.Hadamard(wires=[0])         # wire-0 is |+>
    
    m0 = qml.measure(wires=[0])     # m0 is either 0 or 1    
    qml.cond(m0 == 0,               # If m0 == 0:
        true_fn=qml.RY,             #     Y-rotate wire-1 by theta
        false_fn=qml.RX             # Else: X-rotate wire-1 by theta
    )(theta, wires=[1])             # (Common parameters)
    
    m1 = qml.measure(wires=[1])     # m1 is either 0 or 1    
    qml.cond(m1 == 1,               # If m1 == 1
        true_fn=qml.RX,             #     X-rotate wire-2 by theta
        false_fn=qml.RZ             # Else: Z-rotate wire-2 by theta
    )(theta, wires=2)               # (Common parameters)
    
    return qml.counts()

########################################

def main():

    print('The sample counts for output states [000, ..., 111] are:')
    # Result = {'000': 125, '001': 50, '010': 50, '100': 150, '101': 50, '110': 75}
    # N.B. It sums to 500.
    print(circuit(np.pi / 3))

########################################

if __name__ == '__main__':
    main()
