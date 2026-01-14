############################################################
#
# Author: Prachya Boonkwan
# Affiliation: SIIT, Thammasat Univeristy
# License: CC-BY-NC 4.0
#
############################################################

import pennylane as qml
from pennylane import numpy as np

wires = ['x1', 'x2']
dev = qml.device('default.qubit', wires=wires)

##################################################

# Grounding Hamiltonian: H_G = - X(x1) - X(x2)
hmlt_grounding = qml.Hamiltonian([-1, -1], [qml.X(wires='x1'), qml.X(wires='x2')])
# Problem Hamiltonian: H_P = - Z(x1) Z(x2)
hmlt_problem = qml.Hamiltonian([-1], [qml.Z(wires='x1') @ qml.Z(wires='x2')])

# Total number of steps
no_steps = 100

# Maximum time
t_max = 10

##################################################

# One step of adiabatic transition
def adiabatic_transition(t, t_max, hmlt_grounding, hmlt_problem):
    return (1 - t / t_max) * hmlt_grounding + (t / t_max) * hmlt_problem

@qml.qnode(dev, shots=1000)
def circuit():
    # Ground state = |+>
    qml.Hadamard(wires='x1')
    qml.Hadamard(wires='x2')
    # Adiabatic evolution
    delta_t = t_max / no_steps
    for i in range(no_steps):
        # Compute the Hamiltonian for state transition t
        t = i * delta_t
        hmlt_t = adiabatic_transition(t, t_max, hmlt_grounding, hmlt_problem)
        # Perform state transition with the precomputed Hamiltonian
        qml.ApproxTimeEvolution(hmlt_t, time=delta_t, n=1)
    # Result measurement
    return qml.probs(wires=wires)

##################################################

def main():
    probs = circuit()
    print(f'State probability:\n{probs}')

##################################################

if __name__ == '__main__':
    main()
