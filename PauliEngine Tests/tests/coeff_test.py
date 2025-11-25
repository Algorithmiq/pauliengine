import PauliEngine
import random

def generate_paulistring(length):
    result = {}
    paulis = ["X", "Y", "Z", "I"]
    for i in range(length):
        result[i] = random.choice(paulis)
    return result

pauli_data = generate_paulistring(10)
ps1 = PauliEngine.PauliString(pauli_data, -1)
ps2 = PauliEngine.PauliString(pauli_data, 1)
ps3 = PauliEngine.PauliString(pauli_data, 1)

print(ps2.get_coeff())

ps2.set_coeff(-1)

print(ps2.get_coeff())

print(ps1 == ps2)
print(ps1.equals(ps2))
print(ps1.equals(ps3))
print(ps1 == ps3)
