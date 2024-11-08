import numpy as np
import ust


def rescalate(vertexs):
    re_vers = []
    for i in vertexs:
        v1 = 2*i+1
        re_vers.append(v1)
    return re_vers


class Dualgraph:
    """
    Clase que a partir de un grafo de paralelepipedo regular, 
    genera una base para hacer el dual.

    Params:
        shape (tuple[int]): Dimensionalidad del grafo base a generar.
        start (int, optional): Nodo raíz inicial del grafo para hacer el arbol.
    """
    def __init__(self, shape, start=None):
        """
        Attributes:
            shape (tuple(int)): Dimensionalidad del grafo dual.
            grid (np.array(boolean)): Malla usada como la base
            graph (Grafo): Grafo base.
        """
        # Se genera el grafo original
        g = ust.Grafo(shape, start)
        fil, col = shape
        # Se genera el grafo que permita recorrer los elementos
        self.shape = (2*fil+1, 2*col+1)
        self.grid = np.zeros(2*fil+1, 2*col+1)
        self.graph = g

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
        # Le cambia el valor a 1 para que sea reconocido como 1 vertice parte del arbol de raíz
        if len(vertex.shape) > 1:
            for vertice in vertex:
                self.grid[tuple(vertice)] = 1
        else:
            self.grid[tuple(vertex)] = 1

    def reescalategraph(self):
        list = self.graph.wilson()
        count = 0
        for i in list:
            if (count//2) == 1:
                # ahora deberia comenzar con el reescalamiento
                a = len(i)
                b = rescalate(i)
                for j in range(0, a-1):
                    first = b[j]
                    second = b[j+1]
                    prop = first + (second - first)/2
                    self.append([first, prop, second])

    def dualed(self):
        dual = np.array(np.nonzero(1 - self.grid))
        self.grid = dual
