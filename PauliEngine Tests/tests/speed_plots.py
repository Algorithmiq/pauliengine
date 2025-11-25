import random
import time
import matplotlib.pyplot as plt
import PauliEngine

from openfermion import QubitOperator
from tequila import QubitHamiltonian

testing = []
result_pauli = []
result_ham = []
def generate_random_paulistring(length):
    paulis = ["X", "Y", "Z", "I"]
    result = []
    for i in range(length):
        pauli = random.choice(paulis)
        if pauli != "I": 
            result.append((i, pauli))
    return tuple(result)

def generate_random_qubit_hamiltonian(size, pauli_length):
    coeffs = [1.0, -1.0, 1j, -1j]
    qubit_op = QubitOperator()
    for _ in range(size):
        key = generate_random_paulistring(pauli_length)
        if key:  
            qubit_op += QubitOperator(key, random.choice(coeffs))
    return QubitHamiltonian(qubit_operator=qubit_op)

def generate_paulistring(length):
    result = {}
    paulis = ["X", "Y", "Z", "I"]
    for i in range(length):
        current = random.choice(paulis)
        if current != "I":
            result[i] = current
    return result

def generate_Hamiltonian(size, pauli_length):
    coeff = [1.0, -1.0, 1j, -1j]
    result = []
    random.seed(42)
    for _ in range(size):
        result.append((random.choice(coeff), generate_paulistring(pauli_length)))
    return PauliEngine.QubitHamiltonian(result)

def benchmark_operation(operation_fn, *args, **kwargs):
    start = time.time()
    operation_fn(*args, **kwargs)
    return time.time() - start

def benchmark_vs_size(sizes, fixed_other, generator_fn, operation_fn, plot_name, fixed_type="pauli_length"):
    random.seed(42)
    times = []
    for size in sizes:
        if fixed_type == "pauli_length":
            h1 = generator_fn(size, fixed_other)
            h2 = generator_fn(size, fixed_other)
        else:
            h1 = generator_fn(fixed_other, size)
            h2 = generator_fn(fixed_other, size)
        duration = benchmark_operation(operation_fn, h1, h2)
        times.append(duration)
        if not plot_name in testing:
            testing.append(plot_name)
        print(f"{fixed_type} fix = {fixed_other}, var = {size} → {duration:.2f}s")
    if fixed_type == "pauli_length":
        result_ham.append(times)
    else:
        result_pauli.append(times)
    return times

def plot_results(x_values, *curves, xlabel, title, labels=None):
    if labels is None:
        labels = [f"Variante {i+1}" for i in range(len(curves))]
    for curve, label in zip(curves, labels):
        plt.plot(x_values, curve, marker='o', label=label)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel("Zeit (s)")
    plt.grid(True)
    plt.legend()


hamiltonian_sizes = [1000, 1500, 2000, 2500, 3000]
pauli_lengths = [100, 300, 500, 700, 1000]
fixed_hamiltonian_size = 200
fixed_pauli_length = 300



print()
print("OO-Implementierung")
print("\nBenchmark: Hamiltonian-Größe variiert")

times_binary_ham = benchmark_vs_size(
    hamiltonian_sizes,
    fixed_pauli_length,
    generate_Hamiltonian,
    lambda a, b: a * b,
    "PauliEngine with SymEngine",
    fixed_type="pauli_length"
)

print("\nBenchmark: Pauli-Länge variiert")
times_binary_pauli = benchmark_vs_size(
    pauli_lengths,
    fixed_hamiltonian_size,
    generate_Hamiltonian,
    lambda a, b: a * b,
    "PauliEngine with SymEngine",
    fixed_type="hamiltonian_size"
)

'''


print("\n Benchmark: OpenFermion Hamiltonian-Größe variiert")
times_qubit_ham = benchmark_vs_size(
    hamiltonian_sizes,
    fixed_pauli_length,
    generate_random_qubit_hamiltonian,
    lambda a, b: a * b,
    "OpenFermion",
    fixed_type="pauli_length"
)

print("\n Benchmark: OpenFermion Pauli-Länge variiert")
times_qubit_pauli = benchmark_vs_size(
    pauli_lengths,
    fixed_hamiltonian_size,
    generate_random_qubit_hamiltonian,
    lambda a, b: a * b,
    "OpenFermion",
    fixed_type="hamiltonian_size"
)
'''





plt.figure(figsize=(14, 6))

plt.subplot(1, 2, 1)
plot_results(
    hamiltonian_sizes,
    *result_ham,
    xlabel="Hamiltonian-Size",
    title=f"Runtime vs Hamiltonian-Size\n(fix Pauli string length = {fixed_pauli_length})",
    labels=testing
)

plt.subplot(1, 2, 2)
plot_results(
    pauli_lengths,
    *result_pauli,
    xlabel="Pauli string length",
    title=f"Runtime vs Pauli string size\n(fix Hamiltonian size = {fixed_hamiltonian_size})",
    labels=testing
)

plt.tight_layout()
plt.show()
