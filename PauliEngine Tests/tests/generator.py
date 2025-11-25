import PauliEngine
import random

def generate_paulistring(length):
    """Erzeugt ein dict {index: 'X'/'Y'/'Z'/'I'} für einen PauliString."""
    result = {}
    paulis = ["X", "Y", "Z", "I"]
    for i in range(length):
        result[i] = random.choice(paulis)
    return result
