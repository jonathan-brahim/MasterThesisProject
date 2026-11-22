import networkx as nx
import os
import pandas as pd
from graph_to_circuit import graph_to_circuit
from circuit_to_brickwork import circuit_to_brickwork, get_resources_dict, list_gates, extract_subcircuit
from visualization import visualize_graph, visualize_circuit, visualize_brickwork
from create_graphs import (
    vary_edge_weight,
    create_custom_graph,
    create_complete_graph,
    create_cycle_graph,
    create_path_graph,
    create_bipartite_graph,
)

'''Main code to run the simulation'''

# =============================================================================

# Create different kinds of graphs / List of (graph, name) tuples, add or remove graphs here
K3      = create_complete_graph(3, weight=1.0)
K3_vary = vary_edge_weight(K3, {(0, 1): 1.5, (1, 2): 0.3})

GRAPHS = [
    (create_custom_graph([
            (0, 1, 0.5),
            (1, 2, 1.0),
            (0, 2, 0.8),
        ]),   "custom"),
    (K3,      "K3"),
    (K3_vary, "K3_vary"),
]

# Visualization and save toggles
SHOW_GRAPHS    = True
SHOW_CIRCUITS  = True
SHOW_BRICKWORK = True
SHOW_RESOURCES = True
SAVE_GRAPHS    = True
SAVE_CIRCUITS  = True
SAVE_BRICKWORK = True

# Compare and save resources (depth, etc.) toggles
COMPARE_RESOURCES      = True
SAVE_COMPARISON        = True
SAVE_COMPARISON_FORMAT = "md"  # options: "csv", "md", "txt"

# Apply blinding configuration: identify all gates in circuit and map to indices to blind later on
# None = blind the full circuit
PRINT_GATES = True

BLINDING_CONFIG = {
    "K3":      [[3], [5]],        # gate 3 > brickwork A, gate 5 > brickwork B
    "K3_vary": [[3], [5]],     
    #"K3_vary": [[3, 4], [5]],     # gates 3+4 together > brickwork A, gate 5 > brickwork B
    "custom":  None,              # full circuit > one brickwork (no blinding split)
}


# =============================================================================


def print_resources(name, r):
    """
    Print brickwork resources for a single MasonQ-transpilation result.

    Parameters
    ----------
    name : str
        Name of the graph.
    r : resources
        Resource object returned by circuit_to_brickwork().
    """
    print(f"\n--- Brickwork Resources: {name} ---")
    print(f"  Graph nodes:    {r.graph_nodes}")
    print(f"  Graph depth:    {r.graph_depth}")
    print(f"  Brickwork rows: {r.brick_rows}")
    print(f"  Brickwork cols: {r.brick_columns}")
    print(f"  Qiskit depth:   {r.qiskit_depth}")
    print(f"  Qiskit gates:   {r.qiskit_gates}")
    print(f"  CX gates:       {r.cx_gates}")

def _to_markdown(df):
    """Convert a DataFrame to a markdown table string."""
    cols = ["name"] + list(df.columns)
    rows = [[idx] + list(row) for idx, row in zip(df.index, df.values)]

    header    = "| " + " | ".join(str(c) for c in cols) + " |"
    separator = "| " + " | ".join(["---"] * len(cols)) + " |"
    body      = "\n".join(
        "| " + " | ".join(str(v) for v in row) + " |"
        for row in rows
    )
    return "\n".join([header, separator, body])


def compare_resources(resource_list, savebool=False, save_format="csv"):
    """
    Print and optionally save a comparison table of brickwork resources.

    Parameters
    ----------
    resource_list : list of dict
        List of resource dicts from get_resources_dict().
    savebool : bool
        If True, saves the table to the outputs/ directory.
    save_format : str
        File format: "csv", "md" (markdown), or "txt".
    """

    df = pd.DataFrame(resource_list).set_index("name")

    print("\n--- Resource Comparison ---")
    print(df.to_string())

    if savebool:
        from visualization import OUTPUT_DIR
        os.makedirs(OUTPUT_DIR, exist_ok=True)

        if save_format == "csv":
            path = os.path.join(OUTPUT_DIR, "resource_comparison.csv")
            df.to_csv(path)

        elif save_format == "md":
            path = os.path.join(OUTPUT_DIR, "resource_comparison.md")
            with open(path, "w") as f:
                f.write(_to_markdown(df))

        elif save_format == "txt":
            path = os.path.join(OUTPUT_DIR, "resource_comparison.txt")
            with open(path, "w") as f:
                f.write(df.to_string())

        print(f"Saved to {path}")

def main():
    collected = []

    for graph, name in GRAPHS:

        print(f"\n{'='*40}")
        print(f"Processing: {name} graph/circuit")
        print(f"{'='*40}")

        # Show graphs, convert to circuit, show circuit.
        if SHOW_GRAPHS:
            visualize_graph(graph, title=name, savebool=SAVE_GRAPHS, savename=f"graph_{name}")

        qc = graph_to_circuit(graph)

        if PRINT_GATES:
            list_gates(qc)

        # Visualize the full circuit
        if SHOW_CIRCUITS:
            visualize_circuit(qc, title=f"Full circuit: {name}",
                              savebool=SAVE_CIRCUITS, savename=f"circuit_{name}_full")

        # Apply blinding configuration
        indices = BLINDING_CONFIG.get(name, None)

        if indices is None:
            # no blinding config → treat full circuit as one region
            regions = [("full", qc)]
        else:
            # each inner list is one independent blind region
            regions = [(f"region_{i}", extract_subcircuit(qc, group))
                    for i, group in enumerate(indices)]

        for region_name, qc_region in regions:
            label = f"{name}_{region_name}"
            if SHOW_CIRCUITS:
                visualize_circuit(qc_region, title=label, savebool=SAVE_CIRCUITS, savename=f"circuit_{label}")
            result = circuit_to_brickwork(qc_region, label)
            if SHOW_BRICKWORK:
                visualize_brickwork(result, title=label, savebool=SAVE_BRICKWORK, savename=f"brickwork_{label}")
            if SHOW_RESOURCES:
                print_resources(label, result.resources)
            collected.append(get_resources_dict(label, result))

    # Compares and saves (if desired) resources from brickwork graphs
    if COMPARE_RESOURCES:
        compare_resources(collected, savebool=SAVE_COMPARISON, save_format=SAVE_COMPARISON_FORMAT)

if __name__ == "__main__":
    main()