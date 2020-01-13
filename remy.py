# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""
import math
from collections import defaultdict
from random import *
from collections import deque

# Uncomment the next line if using Python 2.x...
# from __future__ import division
class Rand48(object):
    def __init__(self, seed):
        if (seed < 2 ** 40):
            seed += 2 ** 40
        self.n = seed

    def seed(self, seed):
        self.n = seed

    def srand(self, seed):
        self.n = (seed << 16) + 0x330e

    def next(self):
        self.n = (25214903917 * self.n + 11) & (2 ** 48 - 1)
        return self.n

    def drand(self):
        return self.next() / 2 ** 48

    def lrand(self):
        return self.next() >> 17

    def mrand(self):
        n = self.next() >> 16
        if n & (1 << 31):
            n -= 1 << 32
        return n


class Rand48NoWaste(Rand48):
    def __init__(self, seed):
        super(Rand48NoWaste, self).__init__(seed)
        self.entier = None
        self.bit_count = 0

    def bit_suivant(self):
        if self.bit_count > 0:
            res = self.entier & 1
            self.entier = self.entier >> 1
            self.bit_count -= 1
            return res
        else:
            self.entier = super(Rand48NoWaste, self).mrand()
            self.bit_count += 48
            return self.bit_suivant()

    def gen_n(self, n):
        nb_bits = int(math.ceil(math.log(n, 2)))
        res = 0
        for i in range(nb_bits):
            res = (res << 1) | self.bit_suivant()

        if (res > n):
            return self.gen_n(n)
        return res


class BinTree(object):
    def __init__(self, left=False, right=False):
        self.left = left
        self.right = right

    def is_feuille(self):
        return not self.left

    def set_left(self, left):
        self.left = left

    def set_right(self, right):
        self.right = right

    def __str__(self):
        if (self.is_feuille()):
            return "()"
        return "( " + str(self.left) + " " + str(self.right) + " )"


rand48 = Rand48(156079716630527)
rand48nowaste = Rand48NoWaste(randint(2 ** 40, 2 ** 48))
print(bin(rand48.mrand() & 0xffffffffffff))

"""
for i in range(50):
    print(rand48nowaste.bit_suivant())
"""

print(BinTree(BinTree(), BinTree(BinTree(), BinTree())))


class BinTreeFatherRef(BinTree):
    def __init__(self, father, left=False, right=False):
        super(BinTreeFatherRef, self).__init__(left, right)
        self.father = father

    def set_father(self, f):
        self.father = f


"""
    def __str__(self):
        if self.is_feuille():
            return str(self.ide) + "()"
        return "( " + str(self.ide) + " " + str(self.left) + " " + str(self.right) + " )"
    """


def remy(n, perm=False):
    if n == 0:
        return BinTreeFatherRef(False)

    k = 1

    left = BinTreeFatherRef(False)
    right = BinTreeFatherRef(False)
    root = BinTreeFatherRef(False, left, right)
    left.set_father(root)
    right.set_father(root)
    idNodTree = [root, left, right]

    while (k < n):
        id_chosen = perm[2*(k-1)] if perm else rand48nowaste.gen_n(2 * k)
        print(id_chosen)
        F = idNodTree[id_chosen]

        pleft = perm[2*(k-1)+1] if perm else rand48nowaste.bit_suivant()
        E = BinTreeFatherRef(F.father)

        if F.father:
            if F.father.right is F:
                F.father.set_right(E)
            else:
                F.father.set_left(E)

        F.set_father(E)
        leaf = BinTreeFatherRef(E)
        if pleft == 0:
            E.set_left(F)
            E.set_right(leaf)
        else:
            E.set_right(F)
            E.set_left(leaf)

        idNodTree.append(E)
        idNodTree.append(leaf)
        k = k + 1

    nod = idNodTree[0]
    # find root
    while (nod.father):
        nod = nod.father

    return nod

def gen_perm_aux(n, current_step):
    if current_step >= n:
        return [deque()]
    perms = gen_perm_aux(n, current_step + 1)
    res = []
    for i in range(current_step*2 + 1):
        for perm in perms:
            tmp1 = perm.copy()
            tmp2 = perm.copy()
            tmp1.appendleft(0)
            tmp2.appendleft(1)
            tmp1.appendleft(i)
            tmp2.appendleft(i)
            res.append(tmp1)
            res.append(tmp2)
    return res


def gen_perm(n):
    return gen_perm_aux(n, 1)

def comp(A):
    if A.left == False and A.right == False:
        return ""
    return "(" + comp(A.left) + ")" + comp(A.right)

print(comp(remy(5)))

def generate_all_trees(n):
    dict = defaultdict(lambda : 0)
    perms = gen_perm(n)
    print(len(perms))
    for i in perms:
        dict[comp(remy(n, i))] +=1

    return dict



print(generate_all_trees(4))
print(gen_perm(2))

# print(rand48nowaste.gen_n(48))





































