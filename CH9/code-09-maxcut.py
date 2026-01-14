############################################################
#
# Author: Prachya Boonkwan
# Affiliation: SIIT, Thammasat Univeristy
# License: CC-BY-NC 4.0
#
############################################################

import pennylane as qml
from pennylane import numpy as np
from networkx import Graph

##################################################
# SETTING UP A GRAPH
##################################################

# We create a graph of 5 nodes and 10 edges
no_nodes = 5
no_edges = 10

# We create qubits of the same number as the nodes
wires = list(range(0, no_nodes))
dev = qml.device('default.qubit', wires=wires)

# We sample 10 edges of random source and target nodes
srcidxs = np.random.randint(no_nodes, size=no_edges).data
tgtidxs = np.random.randint(no_nodes, size=no_edges).data
graph = Graph([ (srcidxs[i], tgtidxs[i])
                for i in range(no_edges) ])

# We will use three QAOA layers
circuit_depth = 3

##################################################
# MAXCUT PROBLEM
##################################################

hmlt_loss, hmlt_mixer = qml.qaoa.maxcut(graph)    # Construct the loss and mixer Hamiltonians
                                                  # from our graph

def qaoa_layer(p, m):                             # This is one QAOA layer
    qml.qaoa.cost_layer(p, hmlt_loss)             # First, apply the loss Hamiltonian
    qml.qaoa.mixer_layer(m, hmlt_mixer)           # Then, apply the mixer Hamiltonian

def circuit(params):                              # QAOA circuit
    for i in wires:
        qml.Hadamard(i)
    qml.layer(qaoa_layer, circuit_depth, params[0], params[1])

@qml.qnode(dev, shots=100)
def loss_function(params):                        # Prediction loss yields expectation
    circuit(params)
    return qml.expval(hmlt_loss)

@qml.qnode(dev, shots=100)
def predict(params):                              # Prediction yields state counts
    circuit(params)
    return qml.counts(wires=wires)

##################################################
# QUANTUM APPROXIMATE OPTIMIZATION ALGORITHM
##################################################

def main():
    # Model parameters: always 2 x circuit depth dimensions
    # requires_grad=True means optimizable parameters
    params = np.array(np.random.rand(2, circuit_depth), requires_grad=True)
    
    # Stochastic gradient descent algorithm
    opt = qml.GradientDescentOptimizer(stepsize=0.01)
    no_epochs = 50
    
    # Estimate the parameters for 50 epochs
    for i in range(no_epochs):
        params, loss = opt.step_and_cost(loss_function, params)
        print(f'Loss {i} = {loss}')
    
    # We have obtained the optimal parameters
    print(f'Optimal parameters:\n{params}')
    
    ##### PREDICTION #####
    
    counts = predict(params)
    print(f'Probability distribution:\n{counts}')

##################################################

if __name__ == '__main__':
    main()
