import matplotlib.pyplot as plt
import numpy as np


def reduce_array(array, n):
    idx = np.arange(0, len(array), n)
    return array[idx]


def format_time(array):
    array = array - min(array)
    return array / 60


def save_plot(x, tensione, corrente, temperatura, data_path):
    plt.style.use('bmh')
    x = format_time(x)
    tensione = tensione * 500

    fig, ax = plt.subplots()
    fig.subplots_adjust(right=0.75)

    twin1 = ax.twinx()
    twin2 = ax.twinx()

    # Offset the right spine of twin2.  The ticks and label have already been
    # placed on the right by twinx above.
    twin2.spines.right.set_position(("axes", 1.2))

    p1, = ax.plot(x, tensione, "b-", label="tensione", linewidth=1)
    p2, = twin1.plot(x, corrente, "r-", label="corrente", linewidth=1)
    p3, = twin2.plot(x, temperatura, "g-", label="temperatura", linewidth=1)

    ax.set_ylim(0, 10000)
    twin1.set_ylim(0, 100)
    twin2.set_ylim(0, 100)

    ax.set_xlabel("Time")
    ax.set_ylabel("tensione")
    twin1.set_ylabel("corrente")
    twin2.set_ylabel("temperatura")

    ax.yaxis.label.set_color(p1.get_color())
    twin1.yaxis.label.set_color(p2.get_color())
    twin2.yaxis.label.set_color(p3.get_color())

    tkw = dict(size=4, width=1.5)
    ax.tick_params(axis='y', colors=p1.get_color(), **tkw)
    twin1.tick_params(axis='y', colors=p2.get_color(), **tkw)
    twin2.tick_params(axis='y', colors=p3.get_color(), **tkw)
    ax.tick_params(axis='x', **tkw)

    ax.legend(handles=[p1, p2, p3])

    plt.savefig(data_path, dpi=300)
