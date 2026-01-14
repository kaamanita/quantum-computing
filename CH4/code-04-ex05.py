import pennylane as qml
from pennylane import numpy as np

dev = qml.device('default.qubit', wires=[0, 1])

########################################

@qml.qnode(dev, shots=500)
def circuit_for(iter_no: int, theta0: float, theta1: float):

    @qml.for_loop(0, iter_no, 1)         # for i in range(0, iter_no, 1):
    def loop(i, theta0, theta1):         #     (This is the loop's body)
        qml.RY(theta0, wires=[0])        #     Y-rotate wire-0 by theta0
        qml.RY(theta1, wires=[1])        #     X-rotate wire-1 by theta1
        theta0_new = theta0 / 2          #     Update theta0
        theta1_new = theta1 / 3          #     Update theta1
        return theta0_new, theta1_new    #     Pass theta0 and theta1 to the next iteration

    loop(theta0, theta1)                 # Actually run the loop
    qml.CNOT(wires=[0, 1])
    return qml.counts()

########################################

def main():

    print('The sample counts for output states [00, 01, 10, 11] are:')
    print(circuit_for(10, np.pi / 4, np.pi / 4))

########################################

if __name__ == '__main__':
    main()
