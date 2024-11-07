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
    """
    Borra los loops de una caminata aleatoria dada

    Parámetros
    -----------
    visited : numpy.array[int]
        Caminata como lista de vértices vecinos en el grafo

    dirs :  numpy.array[str]
        Lista de direcciones tomadas en la realización del
        camino en el siguiente formato:
        'u' -> arriba
        'l' -> izquierda
        'r' -> derecha
        'd' -> abajo

    Retorna
    ----------
    lerased_visited: numpy.array[int]
        Caminata creada a partir de visited sin loops

    lerased_dirs: numpy.array[str]
        Lista de direcciones tomadas por el nuevo camino
    """
    # Inicializa el output
    loop_erased = np.zeros((len(visited), 2), dtype=int)
    # Inicializa las direcciones output
    new_dirs = np.empty(len(dirs), dtype=str)
    # Indica hasta donde hemos escrito en el output
    n = 0
    # Separa los vértices que se repiten
    vals, counts = np.unique(visited, return_counts=True, axis=0)
    # Índice del fin del loop borrado en el camino original
    nf = 0
    # Índice del inicio del loop borrado en el camino original
    ni = 0
    while (counts != 1).any():  # Mientras haya vértice repetido (loop)
        set = vals[np.argwhere(counts != 1)]
        # Lista de vértices repetidos
        set = set.reshape(len(set), 2)
        # Se busca el primer vértice repetido según el orden del camino
        # el escaneo comienza desde el fin del ultimo loop borrado
        repetido = ordered_scan(visited[nf:], set)
        # Se guarda el fin del loop anterior como offset
        offset = nf
        # Se busca el siguiente loop y se asignan ni y nf correspondientemente
        ni, nf = offset + np.argwhere(
                             np.logical_and(visited[offset:, 0] == repetido[0],
                                            visited[offset:, 1] == repetido[1]))[np.array([0, -1]), 0]
        # Se copia el camino original al output hasta el inicio del loop nuevo
        loop_erased[n:ni-offset+n] = visited[offset:ni]
        new_dirs[n:ni-offset+n] = dirs[offset:ni]
        # 
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
    
    def lerw(self, start):
        return erase_loops(self.random_walk(start))
