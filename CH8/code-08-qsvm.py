import pennylane as qml
from pennylane import numpy as np

from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

no_qubits = 4
wires = ['x1', 'x2', 'x3', 'x4']
dev = qml.device('lightning.qubit', wires=wires)

########################################
# Dataset Preparation
########################################

def prepare_dataset(no_training, no_testing):
    # Non-linear regression: y = x1 + x2^2 + x3^3 + x4^4 - x0
    # Output: +1 for y >= 0; -1, otherwise
    xs = 2 * np.random.random((no_training + no_testing, 4))
    for i in range(1, no_qubits):
        xs[:, i] = xs[:, i] ** (i + 1)
    coeffs = np.random.random(4)
    threshold = np.random.random() * 6
    ys = np.where(xs @ coeffs - threshold >= 0, +1, -1)
    return xs[:no_training], ys[:no_training], xs[no_training:], ys[no_training:]

xs_train, ys_train, xs_test, ys_test = prepare_dataset(no_training=200, no_testing=50)

########################################
# Quantum Support Vector Machine
########################################

def smv_layer(ftrs, params, wires):
    for wire in wires:
        qml.Hadamard(wires=wire)
    qml.AngleEmbedding(ftrs, wires=wires)
    qml.BasicEntanglerLayers(params, wires=wires)

def ansatz(ftrs, params, wires):
    for j in range(params.shape[0]):
        smv_layer(ftrs, params[j], wires)

@qml.qnode(dev)
def kernel_circuit(ftrs1, ftrs2, params):    # Distance between feature vectors ftrs1 and ftrs2
    ansatz(ftrs1, params, wires=wires)
    qml.adjoint(ansatz)(ftrs2, params, wires=wires)
    return qml.probs(wires=wires)

def kernel(ftrs1, ftrs2, params):    # We separate the kernel function from the quantum circuit
    probs = kernel_circuit(ftrs1, ftrs2, params)
    return probs[0]

def kernel_matrix(A, B, params):        # Distance between each pair of training items
    return np.array([[kernel(a, b, params) for b in B] for a in A])

def prepare_params(no_svmlayers, no_entlayers, no_wires):
    dims = (no_svmlayers, no_entlayers, no_wires)
    params = np.random.uniform(0, 2 * np.pi, dims, requires_grad=True)
    return params

########################################
# Training & Testing
########################################

def main():
    no_svmlayers = 3
    no_entlayers = 2
    init_params = prepare_params(no_svmlayers, no_entlayers, no_qubits)
    quantum_kernel = lambda A, B: kernel_matrix(A, B, init_params)
    
    svm = SVC(kernel=quantum_kernel)        # Training
    svm.fit(xs_train, ys_train)
    
    predictions = svm.predict(xs_test)      # Prediction
    print(f'Accuracy = {accuracy_score(predictions, ys_test)}')

########################################

if __name__ == '__main__':
    main()
