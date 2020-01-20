import os

import numpy

NB = 0
class Arbre:
    def __init__(self, cle, val, F):
        global NB
        self.id = NB
        NB += 1
        self.cle = cle
        self.val = val
        self.fils = F

    def affiche(self):
        if self.cle == '':
            return ' . '
        g = '( ' + self.cle + (',  ' +str(self.val) if self.val != None else '') + '  '
        for f in self.fils:
            g += f.affiche() + ' '
        g += ')'
        return g

    def list_of_words(self,pref):
        res = set()
        if self.cle == "":
            return res
        if self.val == 0:
            res.add(pref + self.cle)
        res = res.union(self.fils[0].list_of_words(pref))
        res = res.union(self.fils[1].list_of_words(pref + self.cle))
        res = res.union(self.fils[2].list_of_words(pref))
        return res

    def search(self,mot):
        if mot=="":
            return False
        if len(self.fils) == 0:
            return False
        if mot[0] < self.cle:
            return self.fils[0].search(mot)
        if mot[0] > self.cle:
            return self.fils[2].search(mot)
        if len(mot) == 1:
            if mot[0] == self.cle and self.val == 0:
                return True
            return False
        else:
            return self.fils[1].search(mot[1:])


    """
    def pprint(self, spaces):
        if self.cle == '':
            return
        if len(self.fils) == 0:
            print(self.cle, end='')
        else:
            self.fils[0].pprint()
            print()
            print(self.cle)
            self.fils[1].pprint()
    """



def gener_feuille():
    return Arbre('', None, [])

def gener_noeud(cle, val, F):
    return Arbre(cle, val, F)


def cons(mot):
    if mot == '':
        return gener_feuille()
    else:
        if len(mot ) == 1:
            return gener_noeud(mot[0], 0, [gener_feuille(), gener_feuille(), gener_feuille()])
        else:
            return gener_noeud(mot[0], None, [gener_feuille(), cons(mot[1:]), gener_feuille()])


def insert(A, mot):
    if mot == '':
        return A
    if A.cle == '':
        return cons(mot)
    if A.cle > mot[0]:
        return gener_noeud(A.cle, A.val, [insert(A.fils[0], mot), A.fils[1], A.fils[2]])
    elif A.cle == mot[0]:
        val = A.val
        if len(mot ) == 1:
            val = 0
        return gener_noeud(A.cle, val, [A.fils[0], insert(A.fils[1], mot[1:]),  A.fils[2]])
    else:
        val = A.val
        #if len(mot ) == 1:
            #val = 0
        return gener_noeud(A.cle, val, [A.fils[0], A.fils[1], insert(A.fils[2], mot)])

def fusion(A, B):
    if A.cle == '':
        return B
    if B.cle == '':
        return A

    if A.cle < B.cle:
        #B.fils[0] may contain nodes of lower value than A.cle, those nodes will be displayed as right sons of a node of higher value (A) which should not be the case
        # search will fail in this case
        return gener_noeud(A.cle, A.val,  [A.fils[0], A.fils[1], fusion(A.fils[2], B)])
    if A.cle > B.cle:
        return gener_noeud(A.cle, A.val,  [fusion(A.fils[0], B), A.fils[1], A.fils[2]])

    if A.val != None:
        val = A.val
    else:
        val = B.val
    return gener_noeud(A.cle, val,  [fusion(A.fils[0], B.fils[0]), fusion(A.fils[1], B.fils[1]), fusion(A.fils[2], B.fils[2])])


l_of_words = None
def creat_Shakespeare(file,nb):
    global l_of_words
    s = set()
    a = Arbre('', None, [])
    if l_of_words is None:
        f = open(file, "r")
        for line in f:
            s.add(line.rstrip("\n\r"))
        l_of_words = list(s)
    #perm = range(len(l_of_words))
    perm = numpy.random.permutation(len(l_of_words))
    for i in perm[:nb]:
        a = insert(a,l_of_words[i])
    return a


for i in range(200):
    a = creat_Shakespeare('/home/fatemeh/PycharmProjects/AAGA/Shakespeare/romeo_juliet.txt',2)
    b= creat_Shakespeare('/home/fatemeh/PycharmProjects/AAGA/Shakespeare/romeo_juliet.txt',2)
    c = fusion(a,b)
    list_a_b = a.list_of_words("").union(b.list_of_words(""))
    list_c = c.list_of_words("")
    try:
        for w in list_a_b:
            print(w)
            assert c.search(w)
    except AssertionError:
        print(list_a_b)
        print(c.affiche())
        print(a.affiche())
        print(b.affiche())
        break
    assert list_c == list_a_b
    print("iteration " + str(i))


a = Arbre('', None, [])
a=insert(a, "fatemeh")
a=insert(a,"fati")
print(a.search("fa"))
#print(c.affiche())

#print(a.affiche())

