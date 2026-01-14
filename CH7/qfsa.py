import pennylane as qml
from pennylane import numpy as np

no_states = 2
markov = { 'a': [ (0, 0,  9/25), (0, 1, 16/25), (1, 1, 3/4), (1, 0, 1/4) ],
           'b': [ (0, 0, 16/25), (0, 1,  9/25), (1, 1, 1/4), (1, 0, 3/4) ] }
input_seq = ['a', 'a', 'b', 'a', 'b', 'b']

########################################

no_qubits_per_state = int(np.ceil(np.log2(no_states)))
state_qubits = list(range(0, no_qubits_per_state))
trans_qubits = list(range(no_qubits_per_state,
                          no_qubits_per_state * (len(input_seq) + 1)))

dev = qml.device('default.qubit', wires = state_qubits + trans_qubits, shots=1000)

########################################

def markov_to_unitary(markov, no_states):
    unitary_tbl = {}
    for symbol in markov:
        mat = np.zeros((no_states, no_states), dtype=np.complex128)
        for (i, j, prob) in markov[symbol]:
            mat[j, i] = prob
        unitary_tbl[symbol] = 2 * mat - np.eye(no_states)
    return unitary_tbl

########################################

@qml.qnode(dev)
def evolution_circuit():
    unitary_tbl = markov_to_unitary(markov, 2)
    for i, symbol in enumerate(input_seq):
        qml.QubitUnitary(unitary_tbl[symbol], wires=state_qubits)
        for j in range(no_qubits_per_state):
            qml.CNOT(wires=[j, (i + 1) * no_qubits_per_state + j])
    return qml.counts(wires=trans_qubits)

########################################

def main():
    print('Sample counts for the final states are:')
    counts = evolution_circuit()
    print(counts)
    # Expected result:
    #   State transitions : Counts
    # { '001010'          : 150,
    #   '001101'          : 425,
    #   '010010'          : 150,
    #   '010101'          : 12.5,
    #   '101010'          : 12.5,
    #   '101101'          : 50,
    #   '110010'          : 150,
    #   '110101'          : 50     }

########################################

if __name__ == '__main__':
    main()
