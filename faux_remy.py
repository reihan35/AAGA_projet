from collections import deque
from collections import  defaultdict

class Node:
    def __init__(self):
        self.val = -2
        self.r = -2
        self.l = -2
        self.p = -2

    def __str__(self):
        return self.val

    def __repr__(self):
        return str(self.p) + " " + str(self.l) + " " + str(self.r)


def change_leaves(tree, a, b):
    parenta = tree[a].p
    parentb = tree[b].p
    if (tree[parenta].r == a):
        tree[parenta].r = b
    else:
        tree[parenta].l = b
    tree[a].p = parentb
    if (tree[parentb].r == b):
        tree[parentb].r = a
    else:
        tree[parentb].l = a
    tree[b].p = parenta


def growing_tree(n, perm):
    tree = []
    for i in range(2 * n + 1):
        tree.append(Node())
    tree[0].r = 1
    tree[0].l = 2
    tree[0].p = -1
    tree[0].val = 1
    tree[1].p = 0
    tree[2].p = 0
    tree[1].r = -1
    tree[1].l = -1
    tree[2].r = -1
    tree[2].l = -1

    for i in range(2, n + 1):
        #print("i vaut " + str(i))
       # print("changing leaves " + str(i - 1) + " and " + str(perm[i - 2] + i - 1))
        change_leaves(tree, i - 1, perm[i - 2] + i - 1)
        tree[i - 1].r = 2 * i - 1
        tree[i - 1].l = 2 * i
        tree[i - 1].val = i
        tree[2 * i - 1].p = i - 1
        tree[2 * i].p = i - 1
        tree[2 * i - 1].r = -1
        tree[2 * i - 1].l = -1
        tree[2 * i].r = -1
        tree[2 * i].l = -1
    return tree


def comp(A, i):
    if A[i].l == -1 and A[i].r == -1:
        return ""
    return "(" + comp(A, A[i].l) + ")" + comp(A, A[i].r)



def gen_perm_aux(n, current_step):
    if current_step > n:
        return [deque()]
    perms = gen_perm_aux(n, current_step + 1)
    res = []
    for i in range(current_step):
        for perm in perms:
            tmp = perm.copy()
            tmp.appendleft(i)
            res.append(tmp)
    return res

def gen_perm(n):
    return gen_perm_aux(n, 2)

def generate_all_trees(n):
    dict = defaultdict(lambda : 0)
    for i in gen_perm(n):
        dict[comp(growing_tree(n,i),0)] +=1

    return dict


print(generate_all_trees(20))
