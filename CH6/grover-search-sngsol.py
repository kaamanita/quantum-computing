import pennylane as qml
from pennylane import numpy as np

soln = np.array([1,1,0,1])                                 # Solution: 1101
no_qubits = len(soln)
wires = range(no_qubits)
dev = qml.device('default.qubit', wires=wires)

########################################

def oracle():                                              # Treat it as a black box

    qml.FlipSign(soln, wires=wires)

def uniform_superposition(wires):
    
    for i in wires:
        qml.Hadamard(wires=i)

@qml.qnode(device=dev, shots=1000)
def grover_search():                    # Note that the solution is always hidden in the oracle
    
    no_iters = int(np.pi / 4 * np.sqrt(2 ** no_qubits))
    uniform_superposition(wires)
    for i in range(no_iters):
        oracle()
        qml.templates.GroverOperator(wires=wires)          # Diffusion operator
    return qml.counts(wires=range(no_qubits))

########################################

def main():

    print('The sample counts for the search result are:')
    counts = grover_search()            # Expected result: {'1101': 1000}
    print(counts)

########################################

if __name__ == '__main__':
    main()
