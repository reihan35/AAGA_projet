from hypothesis.strategies import integers, lists, text
from hypothesis import given

def heapnew():
    return []


def heapempty(heap):
    return not heap


def heappush(heap, value):
    heap.append(value)
    index = len(heap) - 1
    while index > 0:
        parent = (index - 1) // 2
        if heap[parent] > heap[index]:
            heap[parent], heap[index] = heap[index], heap[parent]
            index = parent
        else:
            break


def heappop(heap):
    return heap.pop(0)


@given(lists(integers()))
def test_pop_in_sorted_order(ls):
    h = heapnew()
    for l in ls:
        heappush(h, l)
    r = []
    while not heapempty(h):
        r.append(heappop(h))
    assert r == sorted(ls)

