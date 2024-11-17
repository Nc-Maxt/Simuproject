import numpy as np

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from IPython import display


def animSLE(G, D, A):
    """
    Creates an animation showing G in black, D in red, and updates showing
    the vertices of A in order as green dots.

    Parameters:
    G (numpy.ndarray): Matrix representing vertices of rescalated ST.
    D (numpy.ndarray): Matrix representing vertices of the dual tree.
    A (list): List of indices indicating the order to update vertices.
    """
    G = np.transpose(np.nonzero(G))
    D = np.transpose(np.nonzero(D))
    fig, ax = plt.subplots()
    ax.plot(G[:, 0], G[:, 1], 'ks', ms=10, label='Spanning Tree')
    ax.plot(D[:, 0], D[:, 1], 'rs', ms=10, label='Grafo Dual')
    green_dots, = ax.plot([], [], 'go', lw=8, linestyle='-', label='Curva')
    ax.set_title('Curva $SLE_8$')

    def init():
        green_dots.set_data([], [])
        return green_dots,

    def update(frame):
        x, y = A[frame]
        # x, y = G[idx]
        xdata = green_dots.get_xdata()
        ydata = green_dots.get_ydata()
        xdata.append(x)
        ydata.append(y)
        green_dots.set_data(xdata, ydata)
        return green_dots,

    ani = animation.FuncAnimation(
        fig, update, frames=len(A), init_func=init, blit=True, repeat=False)
    # ax.legend()
    # video = ani.to_html5_video()

    # display.display(display.HTML(video))
    # plt.close()
    ani.save('/home/nacho/simulacion/Simuproject/anim/animation.mp4',
             writer='ffmpeg')
