############################################################
#
# Author: Prachya Boonkwan
# Affiliation: SIIT, Thammasat Univeristy
# License: CC-BY-NC 4.0
#
############################################################

import pennylane as qml
from pennylane import numpy as np

dev = qml.device('default.qubit', wires=[0, 1])

########################################

@qml.qnode(dev, shots=500)
def circuit_while(iter_no: int, theta0: float, theta1: float):

    @qml.while_loop(                     # while:
        lambda t0, t1:                   #     (Terminal condition)
            t0 > 1e-3 and t1 > 1e-3      #     theta0 > 1e-3 and theta1 > 1e-3
    )                                    #
    def loop(theta0, theta1):            #     (This is the loop's body)
        qml.RY(theta0, wires=[0])        #     Y-rotate wire-0 by theta0
        qml.RY(theta1, wires=[1])        #     Y-rotate wire-1 by theta1
        theta0_new = theta0 / 2          #     Update theta0
        theta1_new = theta1 / 3          #     Update theta1
        return theta0_new, theta1_new    #     Pass theta0 and theta1 to the next iteration

    loop(theta0, theta1)                 # Actually run the loop
    qml.CNOT(wires=[0, 1])
    return qml.counts()

########################################

def main():

    print('The sample counts for output states [00, 01, 10, 11] are:')
    print(circuit_while(10, np.pi / 4, np.pi / 4))

########################################

if __name__ == '__main__':
    main()
