import numpy as np


class Stack:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return len(self.items) == 0

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        else:
            raise IndexError("pop from empty stack")

    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        else:
            raise IndexError("peek from empty stack")

    def size(self):
        return len(self.items)


def dfsmatrix(M):
    indices = np.transpose(np.nonzero(1-M))
    num = np.random.randint(0, len(indices))
    i, j = indices[num]
    directions = np.array([[1, 0], [-1, 0], [0, 1], [0, -1]])
    curr = np.array([i, j])
    pila = Stack()
    out = []
    pila.push(curr)
    while not pila.is_empty():
        curr = pila.pop()
        t_curr = tuple(curr)
        if t_curr not in out:
            out.append(t_curr)
        for d in directions:
            next_ = curr + d
            t_next = tuple(next_)
            if M[t_next] == 0 and t_next not in out:
                pila.push(next_)
    return np.array(out)
