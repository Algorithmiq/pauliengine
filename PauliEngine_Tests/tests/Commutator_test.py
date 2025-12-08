import random
from openfermion import QubitOperator, commutator as of_commutator
import PauliEngine


def generate_paulistring(length):
    """Erzeugt ein dict {index: 'X'/'Y'/'Z'/'I'} für einen PauliString."""
    result = {}
    paulis = ["X", "Y", "Z", "I"]
    for i in range(length):
        result[i] = random.choice(paulis)
    return result


def to_openfermion(pauli_dict, coeff):
    """
    Wandelt dein Pauli-Dict in einen OpenFermion-QubitOperator um.
    Beispiel: {0:'X', 1:'I', 2:'Z'} -> QubitOperator('X0 Z2', coeff)
    """
    terms = []
    for qubit, p in pauli_dict.items():
        if p != 'I':  # Identität überspringen
            terms.append(f"{p}{qubit}")
    term_str = ' '.join(terms)
    return QubitOperator(term_str, coeff)


test_amount = 200
coeff = [1.0, -1.0, 1j, -1j]
test_pauli_data = []
test_paulis = []
openfermion_paulistrings = []
counter = 0
pauli_length = 4

fix_pauli_data = generate_paulistring(pauli_length)
fix_pauli = PauliEngine.PauliString(fix_pauli_data, -1)
print(type(fix_pauli.get_coeff()))
fix_of = to_openfermion(fix_pauli_data, -1)

for i in range(test_amount):
    test_pauli_data.append(generate_paulistring(pauli_length))
    coeff_chosen = random.choice(coeff)
    test_paulis.append(PauliEngine.PauliString(test_pauli_data[i], coeff_chosen))
    openfermion_paulistrings.append(to_openfermion(test_pauli_data[i], coeff_chosen))

for i in range (len(test_paulis)):
    print("#################################")
    print("---------Own--------")
    result = fix_pauli.commutator(test_paulis[i])
    result_coeff = PauliEngine.to_complex(result.get_coeff())
    print(result_coeff)
    print("---------AB - BA--------")
    AB = fix_pauli * test_paulis[i]
    BA = test_paulis[i] * fix_pauli
    AB_coeff = PauliEngine.to_complex(AB.get_coeff())
    BA_coeff = PauliEngine.to_complex(BA.get_coeff())
    ab_ba = AB_coeff - BA_coeff 
    print(AB_coeff - BA_coeff)
    print("#################################")
    if result_coeff != ab_ba:
        counter += 1

print(counter)





