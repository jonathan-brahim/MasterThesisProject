import os
import matplotlib.pyplot as plt
import networkx as nx

'''
Visualization functions for graphs, quantum circuits, and brickwork graphs.
'''


OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "outputs")

def visualize_graph(graph, title="", savebool=False, savename=""):
    """
    Visualize a weighted NetworkX graph.

    Parameters
    ----------
    graph : nx.Graph
        Weighted graph to visualize.
    title : str
        Title of the plot.
    savebool : bool
        If True, saves the figure to the outputs.
    savename : str
        Filename (without extension) used when saving. Required if savebool=True.
    """
    pos = nx.spring_layout(graph, seed=2)

    nx.draw(
        graph,
        pos,
        with_labels=True,
        node_color="lightblue",
        node_size=800
    )

    edge_labels = nx.get_edge_attributes(graph, "weight")
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)

    if title:
        plt.title(title)
    if savebool and savename:
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        plt.gcf().savefig(os.path.join(OUTPUT_DIR, f"{savename}.png"))

    plt.show()


def visualize_circuit(qc, title="", savebool=False, savename=""):
    """
    Visualize a Qiskit quantum circuit using matplotlib.

    Parameters
    ----------
    qc : QuantumCircuit
        Qiskit quantum circuit to draw.
    title : str
        Title shown above the circuit diagram. If empty, no title is shown.
    savebool : bool
        If True, saves the figure to the outputs/ directory.
    savename : str
        Filename (without extension) used when saving. Required if savebool=True.
    """
    fig = qc.draw(output="mpl")

    if title:
        fig.suptitle(title)
    if savebool and savename:
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        fig.savefig(os.path.join(OUTPUT_DIR, f"{savename}.png"))

    plt.show()


def visualize_brickwork(result, title="", savebool=False, savename=""):
    """
    Visualize and optionally save a MasonQ brickwork transpilation result.

    Parameters
    ----------
    result : transpile result
        Result returned by circuit_to_brickwork().
    title : str
        Title shown on the brickwork plot. If empty, no title is shown.
    savebool : bool
        If True, saves the figure to the outputs/ directory.
    savename : str
        Filename (without extension) used when saving. Required if savebool=True.
    """
    save_path = None

    if savebool and savename:
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        save_path = os.path.join(OUTPUT_DIR, f"{savename}.png")

    result.plot(save_path=save_path, title=title)