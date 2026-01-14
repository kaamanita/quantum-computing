import pennylane as qml              # Quantum computing
from pennylane import numpy as np    # Classical computing

# Quantum device with two wires (i.e. variables)
dev = qml.device('default.qubit', wires=[0, 1])

########################################

# This is our simple quantum algorithm
@qml.qnode(dev)
def circuit(theta: float):

    # State preparation
    qml.H(wires=[0])            # Hadamard gate on qubit-0
    
    # Computation
    qml.RY(theta, wires=[0])    # Rotate qubit-0 on Axis-Y by theta
    qml.CNOT(wires=[0,1])       # Controlled NOT on qubit-1 with control qubit-0

    # Measurement
    return qml.state()

########################################

def main():
    
    # Let's run our quantum algorithm
    print(circuit(np.pi / 6))

########################################

if __name__ == '__main__':
    main()
