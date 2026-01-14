import pennylane as qml
from pennylane import numpy as np

import torch as T
from torch import nn as N
from torch import optim as O

wires = ['w1', 'w2', 'w3', 'w4']
dev = qml.device('default.qubit', wires=wires)

########################################

@qml.qnode(dev)
def circuit(inputs, params):                         # Quantum circuit
    qml.AngleEmbedding(inputs, wires=wires)          # Encode each input as a quantum state
    qml.BasicEntanglerLayers(params, wires=wires)    # Ansatz
    return [qml.expval(qml.PauliZ(wires=w)) for w in wires]    # Each dimension is in [-1, +1]

########################################

class HybridModel(N.Module):                         # Hybrid classical-quantum model
    def __init__(self):
        super().__init__()
        params_shapes = {"params": (3, 4)}    # Define the shape of parameters `params`
        self.circuit_layer = qml.qnn.TorchLayer(circuit, params_shapes)
        self.softmax = N.Softmax(dim=0)
    def forward(self, inputs):
        outvec = self.circuit_layer(inputs)
        outvec = self.softmax(outvec)
        return outvec

########################################

def main():
    invec = T.tensor([0.0, 0.0, 0.0, 0.0])             # Input vector
    goldstd = T.tensor([0.5, 0.0, 0.5, 0.0])           # Gold-standard output vector
    
    hybrid_model = HybridModel()                       # Our ansatz
    loss_fn = N.MSELoss()                              # The loss function
    opt = O.Adam(hybrid_model.parameters(), lr=0.1)    # SGD algorithm with adaptive gradients
    no_iters = 100                                     # Number of iterations
    
    print('Parameters:')

    # Make prediction before training
    outvec = hybrid_model(invec)
    print(f'Before training: {outvec}')
    
    # Training loop
    for i in range(no_iters):
        outvec = hybrid_model(invec)                   # Make prediction
        loss = loss_fn(outvec, goldstd)                # Compute prediction loss
        opt.zero_grad()                                # Re-estimate the parameters
        loss.backward()
        opt.step()
    
    # Make prediction after training
    outvec = hybrid_model(invec)
    print(f'After training : {outvec}')

########################################

if __name__ == '__main__':
    main()
