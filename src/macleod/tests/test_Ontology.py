import unittest

from Macleod.logical.symbol import (Function, Predicate)
from Macleod.logical.axiom import Axiom
from Macleod.logical.quantifier import (Universal, Existential, Quantifier)
import Macleod.Ontology as Ontology

class OnologyTest(unittest.TestCase):
    """
    Test functionality of Ontology class
    """

    def test_owl_subclass(self):
        a = Predicate('A', ['x'])
        b = Predicate('B', ['x'])
        c = Predicate('C', ['x'])
        d = Predicate('D', ['x'])
        subclass_relation = Axiom(Universal(['x'],  ~d | b | c))

        onto = Ontology("Derp")
        onto.axioms.append(subclass_relation)
        print(onto.to_owl(0))

if __name__ == '__main__':
    unittest.main()
