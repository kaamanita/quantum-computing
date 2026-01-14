############################################################
#
# Author: Prachya Boonkwan
# Affiliation: SIIT, Thammasat Univeristy
# License: CC-BY-NC 4.0
#
############################################################

import pennylane as qml
from pennylane import numpy as np

import torch as T
from torch import nn as N
from torch import optim as O

wires = ['w1', 'w2', 'w3', 'w4']
dev = qml.device('default.qubit', wires=wires)

########################################
# Dataset Preparation
########################################

def prepare_dataset(no_training, no_testing):
    xor_tbl = T.tensor([ (0, 0, 0),
                         (0, 1, 1),
                         (1, 0, 1),
                         (1, 1, 0) ], dtype=T.float)
    training_idxs = np.random.randint(4, size=no_training)
    testing_idxs = np.random.randint(4, size=no_testing)
    training_data = xor_tbl[training_idxs]
    testing_data = xor_tbl[testing_idxs]
    return training_data, testing_data

no_training = 1000
no_testing = 100
training_data, testing_data = prepare_dataset(no_training, no_testing)

########################################
# Hybrid Multilayer Perceptron
########################################

@qml.qnode(dev)
def circuit(inputs, params):
    qml.AngleEmbedding(inputs, wires=wires)
    qml.BasicEntanglerLayers(params, wires=wires)
    outvec = [qml.expval(qml.PauliZ(wires=w)) for w in wires]
    return outvec

class HybridMLP(N.Module):
    def __init__(self, dim_input, dim_output):
        super().__init__()
        (self.dim_input, self.dim_output) = (dim_input, dim_output)
        self.linear1 = N.Linear(self.dim_input, 4)
        self.qlayer = qml.qnn.TorchLayer(circuit, {"params": (3, 4)})
        self.linear2 = N.Linear(4, self.dim_output)
    def forward(self, inputs):
        outvec = self.linear1(inputs)           # Layer 1: Linear(2 -> 4)
        outvec = self.qlayer(outvec)            # Layer 2: Basic entangler
        outvec = self.linear2(outvec)           # Layer 3: Linear(4 -> 1)
        return outvec

xor_model = HybridMLP(dim_input=2, dim_output=1)

########################################
# Training & Testing
########################################

def main():

    ##### Training #####

    loss_fn = N.MSELoss()
    opt = O.Adam(xor_model.parameters(), lr=0.1)
    scheduler = O.lr_scheduler.ExponentialLR(opt, gamma=0.95)        # Simulated annealing
    no_iters = 30
    batch_size = 20
    loss_threshold = 1e-5
    
    for i in range(no_iters):
        np.random.shuffle(training_data)
        total_loss = 0.0
        for j in range(no_training // batch_size):
            batch = training_data[j * batch_size : (j + 1) * batch_size]
            inmat = batch[:, 0:2]
            outmat = xor_model(inmat).flatten()
            goldmat = batch[:, 2]
            loss = loss_fn(outmat, goldmat)
            total_loss += loss.detach().data.item()
            opt.zero_grad()
            loss.backward()
            opt.step()
        scheduler.step()                                             # Reduce the temperature
        print(f'Total loss {i}: {loss.detach().data.item()}')
        if total_loss < loss_threshold: break
    
    ##### Testing #####
    
    no_correct = 0
    
    for j in range(no_testing // batch_size):
        batch = testing_data[j * batch_size : (j + 1) * batch_size]
        inmat = batch[:, 0:2]
        goldmat = batch[:, 2] >= 0.5
        outmat = xor_model(inmat).flatten()
        preds = outmat >= 0.5
        no_correct += (preds == goldmat).sum().item()
    
    print(f'Accuracy: {100 * no_correct / no_testing}')
    # The accuracy is 100%. You should be proud of yourself. ;)

########################################

if __name__ == '__main__':
    main()
