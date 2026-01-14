############################################################
#
# Author: Prachya Boonkwan
# Affiliation: SIIT, Thammasat Univeristy
# License: CC-BY-NC 4.0
#
############################################################

import pennylane as qml
from pennylane import numpy as np

basic_wires = ['b1', 'b2', 'b3', 'b4']
strong_wires = ['s1', 's2', 's3', 's4']
dev = qml.device('default.qubit', wires=basic_wires + strong_wires)

########################################

basic_params = np.random.uniform(0, 2 * np.pi, (2, 4))        # 2 layers, 4 wires
strong_params = np.random.uniform(0, 2 * np.pi, (2, 4, 3))    # 2 layers, 4 wires, 3 angles

########################################

@qml.qnode(dev, shots=100)
def circuit(basic_params, strong_params):
    # Basic entangler requires a L x W matrix of weights
    qml.BasicEntanglerLayers(basic_params, wires=basic_wires)
    # Strong entangler requires a L x W x 3 matrix of weights
    qml.StronglyEntanglingLayers(strong_params, wires=strong_wires)
    return ( qml.counts(wires=basic_wires),
             qml.counts(wires=strong_wires) )

########################################

def main():
    basic_counts, strong_counts = circuit(basic_params, strong_params)
    print('Sample counts for output states of the basic entangler are:')
    print(basic_counts)
    print('\nSample counts for output states of the strong entangler are:')
    print(strong_counts)

########################################

if __name__ == '__main__':
    main()
