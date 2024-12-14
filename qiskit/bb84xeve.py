import random
from qiskit import QuantumCircuit, Aer, execute
import time
start_time = time.time()
random.seed(14931)

# Step 1: Alice generates random secret bits and bases
alice_bits = [random.getrandbits(1) for _ in range(500)]  # Alice's 500 secret bits (0 or 1)
alice_bases = [random.choice(['Z', 'X']) for _ in range(500)]  # Alice's random bases ('Z' or 'X')
print(f"alice bases:")
print("".join(map(str, alice_bases)))
print(f"alice bits:")
print("".join(map(str, alice_bits)))

# Step 2: Encoding Alice's qubits
encoded_qubits = []
for i in range(500):
    bit = alice_bits[i]
    base = alice_bases[i]
    
    qc = QuantumCircuit(1, 1)  # 1 qubit, 1 classical bit

    if base == 'Z':
        if bit == 1:
            qc.x(0)  # Apply X gate to flip the qubit to state |1> if bit is 1
    else:  # base == 'X'
        if bit == 0:
            qc.h(0)  # Apply H gate to put the qubit in |+> state if bit is 0
        else:
            qc.x(0)
            qc.h(0)  # Apply X and H gates to transform to |-> state if bit is 1

    # Append the quantum circuit representing this qubit
    encoded_qubits.append(qc)

# Step 3: Bob chooses random measurement bases
bob_bases = [random.choice(['Z', 'X']) for _ in range(500)]  # Bob's random bases ('Z' or 'X')
print(f"bob bases:")
print("".join(map(str, bob_bases)))

# Step 4: Bob measures Alice's qubits
bob_bits = []
backend = Aer.get_backend('qasm_simulator')  # Using the QASM simulator to simulate measurements

for i in range(500):
    qc = encoded_qubits[i]
    base = bob_bases[i]
    
    if base == 'Z':
        qc.measure(0, 0)  # Measure in the Z basis (no gate needed)
    else:  # base == 'X'
        qc.h(0)  # Apply H gate to change from Z basis to X basis
        qc.measure(0, 0)

    # Execute the quantum circuit on the simulator
    job = execute(qc, backend, shots=1)
    result = job.result()
    counts = result.get_counts()

    # Get the measured bit (most likely outcome)
    measured_bit = int(list(counts.keys())[0], 2)
    bob_bits.append(measured_bit)

# Simulate eavesdropping by altering some bits in Bob's key
num_eavesdrop_bits = 7
for _ in range(num_eavesdrop_bits):
    index = random.randint(0, 499)
    bob_bits[index] = 1 - bob_bits[index]  # Flip the bit to simulate eavesdropping

# Step 6: Generating secret keys
alice_key = [alice_bits[i] for i in range(500) if alice_bases[i] == bob_bases[i]]
bob_key = [bob_bits[i] for i in range(500) if alice_bases[i] == bob_bases[i]]

print(f"alice key:")
print("".join(map(str, alice_key)))
print(f"bob key:")
print("".join(map(str, bob_key)))

# Step 7: Key verification (Eavesdropping detection)
# Randomly select a subset of bits for comparison
subset_size = 50  # Number of bits to compare
indices_to_compare = random.sample(range(len(alice_key)), subset_size)

alice_subset = [alice_key[i] for i in indices_to_compare]
bob_subset = [bob_key[i] for i in indices_to_compare]

print(f"Comparing subsets:")
print(f"Alice's subset: {alice_subset}")
print(f"Bob's subset:   {bob_subset}")

# Check if subsets match
if alice_subset == bob_subset:
    print("Keys match! Secure key established.")
else:
    print("Keys do not match. Possible eavesdropping detected.")

end_time = time.time()
time_taken_ms = (end_time - start_time) * 1000
print(f"Time taken: {time_taken_ms} ms")