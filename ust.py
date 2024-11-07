import numpy as np


direcciones = {
    "u": np.array([0, 1]),
    "d": np.array([0, -1]),
    "l": np.array([-1, 0]),
    "r": np.array([1, 0])
}

str_dir = np.array(["u", "d", "l", "r"])


def ordered_scan(arr, set):
    for i in range(len(arr)):
        if np.equal(set, arr[i]).all(axis=1).any():
            return arr[i]


def erase_loops(visited, dirs):
    loop_erased = np.zeros((len(visited), 2), dtype=int)
    new_dirs = np.empty(len(dirs), dtype=str)
    n = 0
    vals, counts = np.unique(visited, return_counts=True, axis=0)
    nf = 0
    ni = 0
    while (counts != 1).any():
        set = vals[np.argwhere(counts != 1)]
        set = set.reshape(len(set), 2)
        repetido = ordered_scan(visited[nf:], set)
        offset = nf
        ni, nf = offset + np.argwhere(
                             np.logical_and(visited[offset:, 0] == repetido[0],
                                            visited[offset:, 1] == repetido[1]))[np.array([0, -1]), 0]
        loop_erased[n:ni-offset+n] = visited[offset:ni]
        new_dirs[n:ni-offset+n] = dirs[offset:ni]
        n += ni-offset
        vals, counts = np.unique(visited[nf:], return_counts=True, axis=0)
    l = len(visited[nf:])
    loop_erased[n:l+n] = visited[nf:]
    if nf == 0:
        new_dirs[n:l+n] = dirs[nf:]
    else:
        new_dirs[n:l+n-1] = dirs[nf:]
    return loop_erased[0:l+n], new_dirs[0:l+n-1]


class Grafo:
    def __init__(self, shape=(10, 10), start=None):
        self.shape = shape
        self.grid = np.zeros(shape)
        if start is not None:
            self.grid[tuple(start)] = 1
        else:
            i = np.random.randint(0, shape[0])
            j = np.random.randint(0, shape[1])
            self.grid[i, j] = 1

    def isVertex(self, vertex):
        return 0 <= vertex[0] < self.shape[0] and 0 <= vertex[1] < self.shape[1]

    def append(self, vertex):
        assert self.isVertex(vertex)
        self.grid[tuple(vertex)] = 1

    def random_succesor(self, vertex):
        dir = str_dir[np.random.randint(0, 4)]
        while not self.isVertex(vertex+direcciones[dir]):
            dir = str_dir[np.random.randint(0, 4)]
        return vertex+direcciones[dir], dir

    def random_walk(self, start):
        visited = []
        visited.append(start)
        dirs = []
        while True:
            current = visited[len(visited)-1]
            next, dir = self.random_succesor(current)
            visited.append(next)
            dirs.append(dir)
            if self.grid[tuple(visited[-1])]:
                break
        return np.array(visited, dtype=int), np.array(dirs, dtype=str)
