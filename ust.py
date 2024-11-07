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
    """
    Clase que representa un grafo, usada como base para realizar el algoritmo de Wilson y una implementación particular.

    Args:
        shape (tuple[int]): Dimensionalidad del grafo a generar.
        start (int, optional): Nodo raíz inicial del grafo.
    """
    def __init__(self, shape=(10, 10), start=None):
        self.shape = shape
        self.grid = np.zeros(shape)
        #En caso de que el nodo inicial haya sido elegido se le asigna 1 para decir que ya fue visitado
        if start is not None:
            self.grid[tuple(start)] = 1
        #si no, se asigna uno de forma aleatoria entre todos los disponibles
        else:
            i = np.random.randint(0, shape[0])
            j = np.random.randint(0, shape[1])
            self.grid[i, j] = 1


    def isVertex(self, vertex):
        """
        Método que comprueba que la tupla elegida pertenezca al grafo

        Params:
            vertex (tuple[int]): Tupla de dos elementos.

        Return:
            Boolean
        """
        return 0 <= vertex[0] < self.shape[0] and 0 <= vertex[1] < self.shape[1]

    def append(self, vertex):
        """
        Método que agrega nodo al conjunto de los conectados a la raíz

        Params: 
            vertex (tuple[int]): Tupla de dos elementos

        Return:
            None
        """
        #Verifica que sea un vertice perteneciente al grafo
        assert self.isVertex(vertex)
        #Le cambia el valor a 1 para que sea reconocido como 1 vertice parte del arbol de raíz
        self.grid[tuple(vertex)] = 1

    def random_succesor(self, vertex):
        """
        Método que genera el nodo siguiente del actual

        Params: 
            vertex (tuple[int]): Tupla de dos elementos

        Return:
            vertex: el nodo que sigue del inicial
            dir: la dirección en la cual se movió el inicial para llegar al actual
        """
        #se elige la dirección de forma aleatoria entre las 4 posibles 
        dir = str_dir[np.random.randint(0, 4)]
        #se generan posibles sucesores hasta tener un nodo válido 
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
