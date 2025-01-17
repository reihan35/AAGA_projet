import unittest

from hypothesis.stateful import Bundle,rule,RuleBasedStateMachine
from hypothesis.strategies import integers,text
import ternary



class TernaryMachine(RuleBasedStateMachine):
    Arbres = Bundle('arbres')

    def __init__(self):
        super(TernaryMachine, self).__init__()

    @rule(target=Arbres)
    def newArbre(self):
        return ternary.gener_feuille();

    @rule(arbre=Arbres, mot=text())
    def insert(self, arbre, mot):
        ternary.insert(arbre, mot)
        assert arbre.search(arbre, mot)

    @rule (arbre = Arbres, mot=text())
    def search(self, arbre, mot):
        return ternary.search(arbre, mot)

    @rule(target=Arbres, a1=Arbres, a2=Arbres)
    def fusion(self, a1,a2):
        res = ternary.fusion(a1, a2)
        list_a_b = ternary.list_of_words(a1, "").union(ternary.list_of_words(a2, ""))
        for w in list_a_b:
            assert ternary.search(res, w)


TestTernary = TernaryMachine.TestCase
if __name__ == "__main__":
    unittest.main()
print(TestTernary)