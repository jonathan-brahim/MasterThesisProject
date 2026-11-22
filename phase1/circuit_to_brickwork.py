from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from brickwork_transpiler import transpile

'''
Converts a (sub)circuit using the MasonQ-transpiler into a brickwork graph.
'''

def circuit_to_brickwork(qc, name):
    """
        Convert a Qiskit quantum circuit into a brickwork graph.
    
        Parameters
        ----------
        qc : QuantumCircuit
                Circuit to transpile.
    
        Returns
        -------
        result : transpiled result
        """
    
    # Brickwork patterns start every qubit in |+>, so that is the reference input.
    input_state = Statevector.from_label("+" * qc.num_qubits)
    result = transpile(qc, input_state, return_result=True, progress=True)
    return result


def get_resources_dict(name, result):
    """
    Extract brickwork resources into a dictionary.

    Parameters
    ----------
    name : str
        Name of the graph.
    result : transpile result
        Result returned by circuit_to_brickwork().

    Returns
    -------
    dict
    """
    
    r = result.resources
    return {
        "name":         name,
        "graph_nodes":  r.graph_nodes,
        "graph_depth":  r.graph_depth,
        "brick_rows":   r.brick_rows,
        "brick_cols":   r.brick_columns,
        "qiskit_depth": r.qiskit_depth,
        "qiskit_gates": r.qiskit_gates,
        "cx_gates":     r.cx_gates,
    }


def list_gates(qc):
    """
    Print all gates in a circuit with their index, name, qubits and parameters.
    Use this to identify which indices to pass to extract_subcircuit().

    Parameters
    ----------
    qc : QuantumCircuit
        Circuit to inspect.
    """
    print(f"Gates in circuit ({len(qc.data)} total):")
    for i, instruction in enumerate(qc.data):
        qubits = [qc.find_bit(q).index for q in instruction.qubits]
        params = [round(p, 4) for p in instruction.operation.params]
        print(f"  [{i}]  {instruction.operation.name:8s}  qubits={qubits}  params={params}")


def extract_subcircuit(qc, indices):
    """
    Extract a subcircuit from a selection of gate indices.

    Parameters
    ----------
    qc : QuantumCircuit
        Full circuit.
    indices : list of int
        Indices of gates to include (from list_gates).

    Returns
    -------
    sub_qc : QuantumCircuit
    """
    sub_qc = QuantumCircuit(qc.num_qubits)
    for i in indices:
        sub_qc.append(qc.data[i])
    return sub_qc