import PauliEngine
import generator


def test_copy():
        ps = PauliEngine.PauliString(generator.generate_paulistring(20), 1)
        ps_copy = ps.copy()
        assert(ps_copy.equals(ps))
