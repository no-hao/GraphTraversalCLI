from typing import List, Dict


# Section: Graph Visualization and Printing
def print_graph(graph: Dict[str, List[str]]) -> None:
    """
    Prints the graph represented as an adjacency list.

    :param graph: The graph represented as an adjacency list
    """
    for node, neighbors in graph.items():
        neighbors_str = " -> ".join(map(str, neighbors))
        print(f"{node} -> {neighbors_str}")


def visualize_graph(graph: Dict[str, List[str]], path: List[str]) -> None:
    """
    Visualizes the graph and the specified path using NetworkX and Matplotlib.

    :param graph: The graph represented as an adjacency list
    :param path: A list representing a path in the graph
    """
    try:
        import networkx as nx
        import matplotlib.pyplot as plt
    except ImportError:
        print("Visualization requires networkx and matplotlib modules.")
        install_prompt = input(
            "Do you want to install them now? (y/n): "
        ).strip().lower()
        if install_prompt == 'y':
            import subprocess
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", "networkx", "matplotlib"]
            )
            import networkx as nx
            import matplotlib.pyplot as plt
        else:
            print("Visualization aborted.")
            return

    # Now proceed with the visualization
    G = nx.Graph()
    for node, neighbors in graph.items():
        for neighbor in neighbors:
            G.add_edge(node, neighbor)

    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True)
    if path:
        edges_in_path = [(path[i], path[i+1]) for i in range(len(path)-1)]
        nx.draw_networkx_edges(
            G, pos, edgelist=edges_in_path, edge_color='r', width=2, arrows=True
        )
        nx.draw_networkx_nodes(G, pos, nodelist=path, node_color='r')
    plt.show()
