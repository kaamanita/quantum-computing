import pennylane as qml
from pennylane import numpy as np

solns = np.array([ [1,1,0,1], [0,1,0,1] ])                 # Solutions: 1101 and 0101
[no_solns, no_qubits] = solns.shape
wires = range(no_qubits)
dev = qml.device('default.qubit', wires=wires, shots=1000)

########################################

def oracle():
    
    for soln in solns:                                     # We sign-flip on each solution
        qml.FlipSign(soln, wires=wires)

def uniform_superposition(wires):
    
    for i in wires:
        qml.Hadamard(wires=i)
    
@qml.qnode(device=dev)
def grover_search():                    # Observe the change in the iteration number
    
    no_iters = int(np.pi / 4 * np.sqrt(2 ** no_qubits / no_solns))
    uniform_superposition(wires)
    for i in range(no_iters):
        oracle()
        qml.templates.GroverOperator(wires=wires)          # Diffusion operator
    return qml.counts(wires=range(no_qubits))

########################################

def main():

    print('Sample counts for multiple solutions are:')
    counts = grover_search()
    # Expected result: {'0101': 500, '1101': 500}
    print(counts)

########################################

if __name__ == '__main__':
    main()
