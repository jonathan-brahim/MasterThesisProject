import networkx as nx
import qiskit

'''
Code to convert weighted graphs with nodes and weighted edges
(G = (V, E, W)) to a Qiskit quantum circuit. 
'''

def graph_to_circuit(graph):
    """
    Convert a weighted NetworkX graph into a Qiskit quantum circuit.

    Parameters
    ----------
    graph : nx.Graph
        Weighted graph.

    Returns
    -------
    qc : QuantumCircuit
        Qiskit Quantum circuit encoding the graph's edge weights.
    """

    # Number of nodes
    n = graph.number_of_nodes()

    # Initialize quantum circuit
    qc = qiskit.QuantumCircuit(n)

    # Prepare uniform superposition
    for i in range(n):
        qc.h(i)

    # Encode edges using ZZ rotations (this can later be adjusted into other gates perhaps)
    for u, v, data in graph.edges(data=True):
        weight = data.get("weight", 1.0)
        qc.rzz(weight, u, v)

    return qc

