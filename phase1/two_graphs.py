import networkx as nx
from graph_to_circuit import graph_to_circuit, visualize_graph
from circuit_to_brickwork import circuit_to_brickwork

'''
Practice code to create two weighted graphs and convert in quantum circuits. 
'''

def create_two_graphs():
    """
    Create two weighted graphs with identical nodes and edges,
    but one different edge weight.

    Returns
    -------
    G1, G2 : nx.Graph
        Two graphs differing in one edge weight.
    """

    # Create first graph
    G1 = nx.Graph()

    G1.add_weighted_edges_from([
        (0, 1, 0.5),
        (1, 2, 1.0),
        (0, 2, 0.8)
    ])

    # Create an identical copy
    G2 = G1.copy()

    # Change one edge weight
    G2[0][1]["weight"] = 1.2

    return G1, G2


def main():

    # Generate two graphs
    G1, G2 = create_two_graphs()

    # Visualize both graphs
    visualize_graph(G1)
    visualize_graph(G2)

    # Convert graphs to quantum circuits
    qc1 = graph_to_circuit(G1)
    qc2 = graph_to_circuit(G2)

    # Display circuits
    print("Quantum circuit for G1:")
    print(qc1.draw())

    print("\nQuantum circuit for G2:")
    print(qc2.draw())

    # Convert graphs into brickwork graphs
    # Convert quantum circuits into brickwork graphs
    result1 = circuit_to_brickwork(qc1, "G1")
    result2 = circuit_to_brickwork(qc2, "G2")

    # Compare computational resources
    r1 = result1.resources
    r2 = result2.resources

    print("\n--- Brickwork Resource Comparison ---")

    print(f"Graph nodes:    G1={r1.graph_nodes}, G2={r2.graph_nodes}")
    print(f"Graph depth:    G1={r1.graph_depth}, G2={r2.graph_depth}")
    print(f"Brickwork rows: G1={r1.brick_rows}, G2={r2.brick_rows}")
    print(f"Brickwork cols: G1={r1.brick_columns}, G2={r2.brick_columns}")
    print(f"Qiskit depth:   G1={r1.qiskit_depth}, G2={r2.qiskit_depth}")
    print(f"Qiskit gates:   G1={r1.qiskit_gates}, G2={r2.qiskit_gates}")
    print(f"CX gates:       G1={r1.cx_gates}, G2={r2.cx_gates}")
    same_resources = (
        r1.graph_nodes == r2.graph_nodes
        and r1.graph_depth == r2.graph_depth
        and r1.brick_rows == r2.brick_rows
        and r1.brick_columns == r2.brick_columns
    )

    print(f"\nIdentical brickwork resources: {same_resources}")

    
    

if __name__ == "__main__":
    main()