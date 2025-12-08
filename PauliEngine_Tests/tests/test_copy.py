import PauliEngine
import generator

ps = PauliEngine.PauliString(generator.generate_paulistring(20), 1)



ps_copy = ps.copy()

print(ps.to_string())

print(ps_copy.to_string())