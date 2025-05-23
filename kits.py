# from qiskit import QuantumCircuit
# from qiskit_aer import Aer
# from qiskit.visualization import plot_bloch_multivector, plot_state_city
# from numpy import pi
# import matplotlib.pyplot as plt

# # 2x2 image = 4 pixels → use 2 qubits for position, 1 for color
# # Pixel values: [1, 0, 0, 1] → angles: π/2 for 1, 0 for 0
# image_matrix = [
#     [1, 0],
#     [0, 1]
# ]

# # Flatten image row-wise: [1, 0, 0, 1]
# angles = [pi/2 if val == 1 else 0 for row in image_matrix for val in row]

# # Quantum circuit: 2 qubits for position, 1 qubit for color
# qc = QuantumCircuit(3)

# # Step 1: Superposition over all 4 positions (00 to 11)
# qc.h(0)  # position qubit 0
# qc.h(1)  # position qubit 1

# # Step 2: Encode pixel brightness via controlled RY on color qubit
# for i, theta in enumerate(angles):
#     binary = format(i, '02b')           # 00, 01, 10, 11
#     controls = [int(b) for b in binary]

#     # Flip control qubits if control bit is 0
#     for qubit, bit in enumerate(controls):
#         if bit == 0:
#             qc.x(qubit)

#     # Apply controlled RY (encode brightness)
#     qc.mcry(2 * theta, [0, 1], 2)        # RY(2θ) on color qubit (qubit 2)

#     # Undo control flipping
#     for qubit, bit in enumerate(controls):
#         if bit == 0:
#             qc.x(qubit)

# # Step 3: Apply FRQI Negation (flip brightness = -2θ)
# for i, theta in enumerate(angles):
#     binary = format(i, '02b')
#     controls = [int(b) for b in binary]

#     for qubit, bit in enumerate(controls):
#         if bit == 0:
#             qc.x(qubit)

#     # Negate the rotation (2θ - 4θ = -2θ)
#     qc.mcry(-4 * theta, [0, 1], 2)

#     for qubit, bit in enumerate(controls):
#         if bit == 0:
#             qc.x(qubit)

# # Display the quantum circuit
# print(qc.draw('text'))
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from numpy import pi
import numpy as np
import matplotlib.pyplot as plt

# Step 1: Original 2x2 binary image
original_image = np.array([
    [1, 0],
    [0, 1]
])

# Step 2: Negate the image manually (1 → 0, 0 → 1)
negated_binary = 1 - original_image
negated_angles = [pi/2 if val == 1 else 0 for row in negated_binary for val in row]

# Step 3: Build the quantum circuit
qc = QuantumCircuit(3)
qc.h(0)
qc.h(1)

# Encode negated image using Ry rotations
for i, theta in enumerate(negated_angles):
    binary = format(i, '02b')
    controls = [int(b) for b in binary]

    for qubit, bit in enumerate(controls):
        if bit == 0:
            qc.x(qubit)

    qc.mcry(2 * theta, [0, 1], 2)

    for qubit, bit in enumerate(controls):
        if bit == 0:
            qc.x(qubit)

# Step 4: Simulate and extract probabilities
sv = Statevector.from_instruction(qc)
probabilities = sv.probabilities_dict()

# Step 5: Extract brightness per pixel
brightness = [0] * 4
for basis, prob in probabilities.items():
    pos = basis[0:2]
    color = basis[2]
    idx = int(pos, 2)
    if color == '1':
        brightness[idx] += prob

negated_image = np.round(np.array(brightness).reshape(2, 2), 2)

# Step 6: Display images
fig, axs = plt.subplots(1, 2, figsize=(8, 4))

# Original
axs[0].imshow(original_image, cmap='gray', vmin=0, vmax=1)
axs[0].set_title("Original Image")
axs[0].invert_yaxis()

# Negated (quantum)
axs[1].imshow(negated_image, cmap='gray', vmin=0, vmax=1)
axs[1].set_title("Negated Quantum Image")
axs[1].invert_yaxis()

plt.tight_layout()
plt.show()

# Step 7: Print matrices
print("Original Image:\n", original_image)
print("Expected Negated Binary:\n", negated_binary)
print("Simulated Quantum Negated Image:\n", negated_image)
