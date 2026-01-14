############################################################
#
# Author: Prachya Boonkwan
# Affiliation: SIIT, Thammasat Univeristy
# License: CC-BY-NC 4.0
#
############################################################

import pennylane as qml
from pennylane import numpy as np

########################################
# SETTING UP A DISTANCE MATRIX
########################################

no_cities = 4
# distance_matrix = np.random.randint(20, size=(no_cities, no_cities)) + 1
distance_matrix = np.array([ [10, 20, 30, 40],
                             [30, 10, 20, 10],
                             [60, 10, 70, 30],
                             [40, 30, 20, 10] ])

########################################
# SETTING UP THE QUANTUM COMPUTER
########################################

wires = range(no_cities ** 2)
dev = qml.device('lightning.qubit', wires=wires)

def idx_qubit(cityidx, timestep):
    return cityidx * no_cities + timestep

##### TRAVELING SALESMAN PROBLEM #####

def compute_rewards(distance_matrix, no_cities):
    co_pairs = []
    for t in range(no_cities):
        t_next = (t + 1) % no_cities
        for i in range(no_cities):
            for j in range(no_cities):
                if i == j: continue
                idx_i = idx_qubit(i, t)
                idx_j = idx_qubit(j, t_next)
                # N[i,t] * N[j,t+1] = 1/4 (1 - Z[i] - Z[j] + Z[i] * Z[j])
                # We ignore the constant part
                co_pairs.extend([
                    (-0.25 * distance_matrix[i,j], qml.Z(idx_i)),
                    (-0.25 * distance_matrix[i,j], qml.Z(idx_j)),
                    (0.25 * distance_matrix[i,j], qml.Z(idx_i) @ qml.Z(idx_j))
                ])
    penalty = 3 * no_cities**3
    return co_pairs, penalty

def compute_penalty(distance_matrix, no_cities, penalty):
    co_pairs = []
    for i in range(no_cities):
        for t1 in range(no_cities):
            for t2 in range(t1 + 1, no_cities):
                idx_1 = idx_qubit(i, t1)
                idx_2 = idx_qubit(i, t2)
                # We peanlize two 1's in a row/column by
                # adding P / 2 * Z[i] * Z[j]
                co_pairs.append( (0.5 * penalty, qml.Z(idx_1) @ qml.Z(idx_2)) )
    return co_pairs

def compute_loss_hmlt(distance_matrix, no_cities):
    co_pairs_rewards, penalty = compute_rewards(distance_matrix, no_cities)
    co_pairs_penalty = compute_penalty(distance_matrix, no_cities, penalty)
    co_pairs = co_pairs_rewards + co_pairs_penalty
    coeffs = [pair[0] for pair in co_pairs]
    obsvs = [pair[1] for pair in co_pairs]
    return qml.Hamiltonian(coeffs, obsvs)

hmlt_loss = compute_loss_hmlt(distance_matrix, no_cities)
hmlt_mixer = qml.qaoa.x_mixer(wires)

########################################
# QUANTUM CIRCUIT
########################################
    
circuit_depth = 2

def qaoa_layer(p, m):
    qml.qaoa.cost_layer(p, hmlt_loss)
    qml.qaoa.mixer_layer(m, hmlt_mixer)

def circuit(params):
    # Initial state: 1 for each city i and timestep i
    for i in range(no_cities):
        qml.X(idx_qubit(i, i))
    qml.layer(qaoa_layer, circuit_depth, params[0], params[1])

@qml.qnode(dev, shots=100)
def loss_function(params):
    circuit(params)
    return qml.expval(hmlt_loss)

@qml.qnode(dev, shots=100)
def predict(params):
    circuit(params)
    return qml.counts(wires=wires)

########################################
# QUANTUM APPROXIMATE OPTIMIZATION ALGORITHM
########################################

def main():
    
    params = np.array(np.random.rand(2, circuit_depth), requires_grad=True)
    opt = qml.AdamOptimizer(stepsize=0.001)
    no_steps = 10
    
    for i in range(no_steps):
        params, cost = opt.step_and_cost(loss_function, params)
        print(f'Loss {i} = {cost}')
    
    print(f'Optimal parameters:\n{params}')
    
    counts = predict(params)
    print(f'Probability distribution:\n{counts}')

########################################

if __name__ == '__main__':
    main()

##### WARNING: IT TAKES AGES TO TRAIN THE MODEL WITHOUT GPU/QPU #####
