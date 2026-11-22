import networkx as nx

'''
Different functions to create different types of weighted NetworkX graphs.
Each function returns a nx.Graph with weighted edges.
> Custom graphs
> Complete graphs
> Cycle graphs
> Path graphs
> Bi-partite graphs
'''

def vary_edge_weight(graph, edge_weights):
    """
    Return a copy of a graph with one or more edge weights changed.

    Parameters
    ----------
    graph : nx.Graph
        Original graph.
    edge_weights : dict of {(int, int): float}
        Dictionary mapping edges to their new weights,
        e.g. {(0, 1): 1.5, (1, 2): 0.3}.

    Returns
    -------
    G : nx.Graph
        Modified copy, original is unchanged.
    """
    G = graph.copy()
    for (u, v), new_weight in edge_weights.items():
        G[u][v]["weight"] = new_weight
    return G

def create_custom_graph(edges):
    """
    Create a graph from a manual list of (node_1, node_2, weight) tuples.

    Parameters
    ----------
    edges : list of (int, int, float)
        Edge list with weights.

    Returns
    -------
    G : nx.Graph
    """
    G = nx.Graph()
    G.add_weighted_edges_from(edges)
    return G


def create_complete_graph(n, weight=1.0, weights=None):
    """
    Create a fully connected graph on n nodes with weighted edges.

    Parameters
    ----------
    n : int
        Number of nodes.
    weight : float
        Uniform weight assigned to every edge. Used when weights=None.
    weights : list of float, optional
        Per-edge weights in the order (0,1), (0,2), ..., (n-2, n-1).
        Must match the number of edges exactly.

    Returns
    -------
    G : nx.Graph
    """

    G = nx.complete_graph(n)
    edges = list(G.edges())

    for i, (u, v) in enumerate(edges):
        G[u][v]["weight"] = weights[i] if weights is not None else weight

    return G


def create_cycle_graph(n, weight=1.0, weights=None):
    """
    Create a cycle graph on n nodes with weighted edges.

    Parameters
    ----------
    n : int
        Number of nodes.
    weight : float
        Uniform weight assigned to every edge. Used when weights=None.
    weights : list of float, optional
        Per-edge weights in order around the cycle (0,1), (1,2), ..., (n-1,0).
        Must match the number of edges exactly.

    Returns
    -------
    G : nx.Graph
    """
    G = nx.cycle_graph(n)
    edges = list(G.edges())

    for i, (u, v) in enumerate(edges):
        G[u][v]["weight"] = weights[i] if weights is not None else weight

    return G


def create_path_graph(n, weight=1.0, weights=None):
    """
    Create a path graph on n nodes with weighted edges.

    Parameters
    ----------
    n : int
        Number of nodes.
    weight : float
        Uniform weight assigned to every edge. Used when weights=None.
    weights : list of float, optional
        Per-edge weights along the path (0,1), (1,2), ..., (n-2, n-1).
        Must match the number of edges exactly: n-1 weights.

    Returns
    -------
    G : nx.Graph
    """
    
    G = nx.path_graph(n)
    edges = list(G.edges())

    for i, (u, v) in enumerate(edges):
        G[u][v]["weight"] = weights[i] if weights is not None else weight

    return G


def create_bipartite_graph(n1, n2, weight=1.0, weights=None):
    """
    Create a complete bipartite graph K_{n1, n2} with weighted edges.

    Parameters
    ----------
    n1 : int
        Number of nodes in the first partition.
    n2 : int
        Number of nodes in the second partition.
    weight : float
        Uniform weight assigned to every edge. Used when weights=None.
    weights : list of float, optional
        Per-edge weights in NetworkX edge order.
        Must match the number of edges exactly: n1 * n2 weights.

    Returns
    -------
    G : nx.Graph
    """
    G = nx.complete_bipartite_graph(n1, n2)
    edges = list(G.edges())

    for i, (u, v) in enumerate(edges):
        G[u][v]["weight"] = weights[i] if weights is not None else weight

    return G