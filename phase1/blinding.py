from qiskit.quantum_info import Statevector
import numpy as np

'''
Code to simulate Partial Blind Quantum Computing (PBQC).
Step 1: MBQC simulation and verification against Qiskit.
'''


def simulate_mbqc(result):
    """
    Run the Graphix pattern simulation and return the output state.

    Parameters
    ----------
    result : transpile result
        Result returned by circuit_to_brickwork().

    Returns
    -------
    state : Graphix state object
        Output state after simulating the brickwork pattern.
    """
    state = result.pattern.simulate_pattern()
    return state


def verify_mbqc(qc, result):
    """
    Compare the MBQC output state with a direct Qiskit statevector simulation.
    States are compared via overlap |<ψ_qiskit|ψ_mbqc>|, which equals 1
    if the two states are identical up to global phase.

    Parameters
    ----------
    qc : QuantumCircuit
        The original Qiskit circuit (before brickwork transpilation).
    result : transpile result
        Result returned by circuit_to_brickwork().

    Returns
    -------
    overlap : float
        Absolute overlap between the two states. 1.0 = perfect match.
    """
    sv_qiskit = Statevector(qc).data               # numpy array from Qiskit
    sv_mbqc   = simulate_mbqc(result).statevector  # check exact attribute name

    overlap = abs(np.dot(sv_qiskit.conj(), sv_mbqc))
    print(f"  Overlap |<ψ_qiskit|ψ_mbqc>| = {overlap:.6f}  ({'✓ match' if overlap > 0.999 else '✗ mismatch'})")
    return overlap