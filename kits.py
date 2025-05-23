from qiskit import QuantumCircuit
from qiskit_aer import Aer
from qiskit.visualization import plot_bloch_multivector, plot_state_city
from numpy import pi
import matplotlib.pyplot as plt

# Define angles for the image matrix [1, 0, 0, 1]
angles = [pi/2, 0, 0, pi/2]  # Corresponding to pixel values

# Initialize quantum circuit: 2 qubits for encoding position, 1 qubit for color
qc = QuantumCircuit(3)

# Step 1: Apply Hadamard to position qubits to create superposition
qc.h(0)
qc.h(1)

# Step 2: Use controlled rotation to encode pixel color (angle)
for i, theta in enumerate(angles):
    binary = format(i, '02b')
    controls = [int(b) for b in binary]

    # Apply X to invert control qubits if bit is 0
    for qubit, bit in enumerate(controls):
        if bit == 0:
            qc.x(qubit)

    # Apply controlled RY rotation to color qubit (qubit 2)
    qc.mcry(2 * theta, [0, 1], 2)

    # Undo X to restore original state
    for qubit, bit in enumerate(controls):
        if bit == 0:
            qc.x(qubit)

# Apply Negation: flip the sign of theta → controlled-RY(-2θ)
for i, theta in enumerate(angles):
    binary = format(i, '02b')
    controls = [int(b) for b in binary]

    # Apply X to invert control qubits if bit is 0
    for qubit, bit in enumerate(controls):
        if bit == 0:
            qc.x(qubit)

    # Apply controlled RY with negative angle
    qc.mcry(-4 * theta, [0, 1], 2)  # -2θ extra to negate previous rotation

    # Undo X to restore original state
    for qubit, bit in enumerate(controls):
        if bit == 0:
            qc.x(qubit)

# Draw the circuit
# qc.draw('mpl')
print(qc.draw('text'))
