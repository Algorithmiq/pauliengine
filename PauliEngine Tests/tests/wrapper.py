import PauliEngine as pe
import typing

class PauliString():

        pauliString_object = 0

        '''
        Constructor for PauliString objects
        Accepts following formats:
        tuple(complex: coeff, dict(int : str) : pauliString)
        tuple(string: coeff, dict(int : str) : pauliString)
        tuple(expression: coeff, dict(int : str) : pauliString)
        OpenFermion format
        '''
        def PauliString(self, data):
                self.pauliString_object = pe.PauliString(data)

        def key_openfermion(self):
                """
                Convert into key to store in Hamiltonian
                Same key syntax than openfermion
                :return: The key for the openfermion dataformat
                """
                return tuple(self.pauliStrnig_object.key_openfermion())
        def __init__(self, data, coeff):
                self.pauliStrnig_object = pe.PauliString(data, coeff)


        def __eq__(self, other):
                return self.pauliStrnig_object == other.pauliString_object
        
        def __mul__(self, other):
                return self.pauliStrnig_object * other.pauliString_object

        def __imul__(self, other):
                self.pauliString_object *= other.pauliString_object

        def __str__(self):
                return self.pauliString_object.to_string()
        
        def __repr__(self):
                return self.pauliString_object.to_string()

        def is_all_z(self):
                return self.pauliString_object.is_all_z()
        
        def to_dictionary(self):
                return self.pauliString_object.to_dictionary()
        
        def map_qubits(self, qubit_map):
                return self.pauliString_object.map_qubits(qubit_map)
        
        '''
        Computes the commutator for two PauliStrings
        :returns: 0 if PauliStrings commutate
                  PauliString with doubled Coefficient of not
        '''
        def commutator(self, other):
                return PauliString(self.pauliString_object.commutator(other.pauliString_object))
        
        '''
        Returns the Coefficient of the PauliString
        Expression: Only Available, if Symengine is present
        Complex: If Symengine is not present
        '''
        def coeff(self):
                if isinstance(self.pauliString_object.get_coeff(), pe.Expression):
                        return pe.to_complex(self.pauliString_object.get_coeff())
                else:
                        return self.pauliString_object.get_coeff()
        
        def trace_out_qubits(self, qubits, states=None):
                """
                See trace_out_qubits in QubitHamiltonian
                Parameters
                ----------
                qubits
                qubits to trace out
                states
                states a|0> + b|1> as list of tuples of the a,b coefficients. Default is just |0>.
                Returns
                -------
                traced out PauliString
                """
                if states is None:
                        states = [(1.0, 0.0)]*len(qubits)
                return self.pauliString_object.trace_out_qubits(qubits, states)
        



class QubitHamimltonian():

        hamiltonian_object = 0

        '''
        Constructor for QubitHamiltonian objects.
        Accepts following formats
        list[PauliString]
        list[tuple(complex: coeff, dict(int : str) : pauliString)]
        list[tuple(string: coeff, dict(int : str) : pauliString)]
        list
        '''
        def QubitHamiltonian(self, data):
                self.hamiltonian_object = pe.QubitHamiltonian(data)

        def __add__(self, other):
                return self.hamiltonian_object + other.hamiltonian_object
        
        def __mul__(self, other: complex, QubitHamiltonian):
                return self.hamiltonian_object * other.hamiltonian_object
        
        def trace_out_qubits(self, qubit_list, state_list):
                assert len(qubit_list) == len(state_list)
                return self.hamiltonian_object.trace_out_qubits(qubit_list, state_list)


        '''
        Parse the QubitHamiltonian into the format: list[tuple(complex / Expression : coeff, dict(int : str) : pauliString)]
        '''
        def parse_python_format(self):
                return self.hamiltonian_object.parse_python_format()
        
        def __str__(self):
                return self.hamiltonian_object.to_string()
        
        def __repr__(self):
                return self.hamiltonian_object.to_string()
        
        '''
        Differentiation of all PauliStrings in the Hamiltonian by the given variable
        Only Available, if Symengine is present
        '''

        def diff(self, symbol):
                #if symbol.__name__ == tq_variable:
                #       symbol = str(symbol)

                return self.QubitHamiltonian.diff(symbol)
        '''
        Replaces all variables with a given value in the substitution_map.
        Substitution_map has following format:
        dict(string: variable_name, complex: substitute_with)
        Only Available, if Symengine is present
        '''
        def subs(self, substitution_map):
                return self.QubitHamiltonian.subs(substitution_map)
        

        


