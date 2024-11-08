import numpy as np
import ust


class dualgraph:
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

