import numpy as np
import ust


def rescalate(vertexs):
    re_vers = []
    for i in vertexs:
        v1 = 4*i+2
        re_vers.append(v1)
    return re_vers


class dualgraph:
    """
    Clase que a partir de un grafo de paralelepipedo regular,
    genera una base para hacer el dual.

    Attributes:
        shape (tuple[int]): Dimensionalidad del grafo base a generar.
        grid (np.array(boolean)): Malla usada como la base
        graph (Grafo): Grafo base.

    """
    def __init__(self, shape, start=None):
        """
        Attributes:
            shape (tuple(int)): Dimensionalidad del grafo dual.
            start (int, optional): Nodo razo para hacer el arbol.
        """
        # Se genera el grafo original
        g = ust.Grafo(shape, start)
        fil, col = shape
        # Se genera el grafo que permita recorrer los elementos
        self.shape = (4*fil+1, 4*col+1)
        self.grid = np.zeros(4*fil+1, 4*col+1)
        self.graph = g
        self.actives = []

    def append(self, vertex):
        """
        Método que agrega nodo al conjunto de los conectados a la raíz

        Params:
            vertex (tuple[int]): Tupla de dos elementos

        Return:
            None
        """
        # Verifica que sea un vertice perteneciente al grafo
        assert self.isVertex(vertex)
        # Le cambia el valor a 1 para que sea reconocido como 1 vertice parte
        # del arbol de raíz
        if len(vertex.shape) > 1:
            for vertice in vertex:
                self.grid[tuple(vertice)] = 1
        else:
            self.grid[tuple(vertex)] = 1

    def isVertex(self, vertex):
        return 0

    def reescalategraph(self):
        paths = self.graph.wilson()
        count = 0
        for i in paths:
            # los pares son los que tienen caminos (no hay ciclos)
            if (count//2) == 1:
                # ahora comienza con el reescalamiento
                a = len(i)
                b = rescalate(i)
                for j in range(0, a-1):
                    first = b[j]
                    fourth = b[j+1]
                    movs = (fourth - first)/4
                    second = first + movs
                    third = first + 2*movs

                    self.actives.append(first)
                    self.actives.append(second)
                    self.actives.append(third)
                    self.append([first, second, third])

    """
    def dualed(self):
        dual = np.array(np.nonzero(1 - self.grid))
        self.grid = dual
    """