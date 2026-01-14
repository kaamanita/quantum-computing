import pennylane as qml
from pennylane import numpy as np
from pennylane.numpy import random as rnd
from fractions import Fraction

no_targets, no_counts = 8, 8
no_qubits = no_targets + no_counts
wires = range(no_qubits)
counting_wires = range(no_counts)
target_wires = range(no_counts, no_qubits)

dev = qml.device('default.qubit', wires=wires)

########################################

def prepare_primes(n):
    flags = np.ones(n, dtype=bool)
    flags[0] = flags[1] = False
    for i in range(2, n):
        if flags[i]:
            for j in range(2 * i, n, i):
                flags[j] = False
    return np.arange(n)[flags]

primes = prepare_primes(2 ** no_targets)

########################################

def factorize_shor(n, primes):
    if n == 1:
        return np.array([n])
        
    potential_factors = primes[primes <= np.sqrt(n)]
    for a in potential_factors:
    
        # Classical factorization
        k = np.gcd(n, a)
        if k != 1:
            return np.hstack([ factorize_shor(k, primes), factorize_shor(n // k, primes) ])
        
        # Quantum speedup
        r = find_order(n, a)
        if r % 2 == 1: continue
        
        k = np.gcd(n, a ** (r // 2) - 1)
        if k != 1:
            return np.hstack([ factorize_shor(k, primes), factorize_shor(n // k, primes) ])
    
    return np.array([n])

########################################

def find_order(n, a):
    probs = order_finding_circuit(n, a)
    idx = int(np.argmax(probs))
    frac = Fraction(idx, 2 ** no_counts)
    r = frac.denominator
    return r

def modulo_matrix(a, power, n):
    dims = 2 ** no_targets
    mat = np.zeros((dims, dims), dtype=np.complex128)
    factor = np.mod(np.power(a, power), n)
    for i_input in range(dims):
        if i_input < n:
            i_output = (factor * i_input) % n
        else:
            i_output = i_input
        mat[i_output, i_input] = 1.0
    return mat

def apply_power_modulo(a, power, n, ctrl_wires, tgt_wires):
    mat = modulo_matrix(a, power, n)
    qml.ctrl(qml.QubitUnitary(mat, wires=tgt_wires), ctrl_wires)

########################################

@qml.qnode(dev)
def order_finding_circuit(n, a):
    init_state = np.zeros(2 ** no_qubits)
    init_state[0] = 1.0
    qml.StatePrep(init_state, wires=wires)
    
    for i in counting_wires:
        qml.Hadamard(wires=i)
    
    for k, ctrl in enumerate(counting_wires):
        power = 2 ** k
        apply_power_modulo(
            a, power, n,
            ctrl_wires=[ctrl], tgt_wires=target_wires
        )
    
    qml.adjoint(qml.QFT)(wires=counting_wires)
    
    return qml.probs(wires=counting_wires)

########################################

def main():
    print('Factorization of 152 is:')
    print(factorize_shor(152, primes))
    # Expected result: [ 2  2  2 19]

########################################

if __name__ == '__main__':
    main()
