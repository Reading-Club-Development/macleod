import unittest

from Macleod.logical.symbol import (Function, Predicate)
from Macleod.logical.axiom import Axiom
from Macleod.logical.quantifier import (Universal, Existential, Quantifier)
import Macleod.Ontology as Ontology

import Macleod.scripts.parser as Parser

class OnologyTest(unittest.TestCase):
    """
    Test functionality of Ontology class
    """

    def test_parse(self):
        a = Predicate('A', ['x'])
        b = Predicate('B', ['x'])
        c = Predicate('C', ['x'])
        d = Predicate('D', ['x'])
        subclass_relation = Axiom(Universal(['x'],  ~d | b | c))

        onto = Ontology("Derp")
        onto.axioms.append(subclass_relation)

        Parser.parse_clif("rcc_basic.clif")

if __name__ == '__main__':
    unittest.main()
