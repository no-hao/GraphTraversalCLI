import csv
from collections import deque
from time import time
from typing import Dict, List, Tuple, Optional

# Constants
EXIT_COMMAND = 'exit'
CSV_FILE_EXTENSION = '.csv'

# Error handling constants
MAX_TRAVERSAL_QUEUE_SIZE = 10000  # Adjust as necessary
TRAVERSAL_TIMEOUT_SECONDS = 900  # Adjust as necessary in seconds


# Section: Input and Output utilities
def get_input(prompt: str) -> str:
    """
    Gets user input with a given prompt.

    :param prompt: The prompt to display to the user
    :return: The user input as a string
    """
    user_input = input(prompt)
    if user_input.lower() == EXIT_COMMAND:
        exit()
    return user_input



def read_graph_from_csv(file_path: str) -> Tuple[Dict[str, List[str]], Optional[str]]:
    """
    Reads the graph from a CSV file and returns it as an adjacency list.

    :param file_path: The path to the CSV file
    :return: A tuple containing the adjacency list and an error message if any
    """
    adjacency_list = {}
    try:
        with open(file_path, 'r', encoding='utf-8-sig') as file:
            reader = csv.reader(file)
            for row in reader:
                node = row[0]
                adjacency_list[node] = [neigh for neigh in row[1:] if neigh]
        return adjacency_list, None
    except Exception as e:
        return None, str(e)


# Section: User Input Handling
def get_user_input(graph: Dict[str, List[str]]) -> Tuple[str, str, Dict[str, List[str]], bool, bool, bool, bool, bool]:
    """
    Gets user input for various options in the CLI.

    :param graph: The graph represented as an adjacency list
    :return: A tuple containing user inputs for various options
    """
    while True:
        try:
            start_node = get_input("Start node (or type 'exit' to quit): ")
            end_node = get_input("End Node (or type 'exit' to quit): ")

            if start_node not in graph or end_node not in graph:
                raise ValueError("Node ID out of range")

            print_flag_input = get_input(
                "Enter p to print the graph, or type 'exit' to quit, or press Enter to continue: "
            )

            debug_flag_input = get_input(
                "Enter d to enable debug mode (verbose output), b to debug BFS, f to debug DFS, "
                "or type 'exit' to quit, or press Enter to continue: "
            )
            debug_flag = debug_flag_input == 'd'
            debug_bfs = debug_flag_input == 'b'
            debug_dfs = debug_flag_input == 'f'

            visualize_flag_input = get_input(
                "Enter v to visualize the graph and the path found, or type 'exit' to quit, or press Enter to continue: "
            )

            return (
                start_node, end_node, graph,
                print_flag_input.lower() == 'p',
                debug_flag,
                visualize_flag_input.lower() == 'v',
                debug_bfs,
                debug_dfs
            )
        except ValueError as e:
            print(f"Invalid input: {e}. Please try again.")
        except SystemExit:
            raise


# Section: Graph Traversal Algorithms
def reconstruct_path(predecessor: Dict[str, str], start_node: str, end_node: str) -> Optional[List[str]]:
    """
    Reconstructs the path from start_node to end_node using the predecessor dictionary.

    :param predecessor: A dictionary where the key is a node and the value is the predecessor of that node
    :param start_node: The start node for the path
    :param end_node: The end node for the path
    :return: A list representing the path from start_node to end_node (or None if no path found)
    """
    path = deque()
    current_node = end_node
    while current_node is not None:
        path.appendleft(current_node)
        current_node = predecessor.get(current_node)
    if path[0] == start_node:
        return list(path)
    else:
        return None


def bfs(graph: Dict[str, List[str]], start_node: str, end_node: str, debug: bool = False, debug_bfs: bool = False) -> Optional[List[str]]:
    """
    Performs breadth-first search (BFS) on the graph to find the shortest path
    from start_node to end_node.

    :param graph: The graph represented as an adjacency list
    :param start_node: The start node for the BFS
    :param end_node: The end node for the BFS
    :param debug: A flag indicating whether to print general debug information
    :param debug_bfs: A flag indicating whether to print BFS specific debug information
    :return: A list representing the path from start_node to end_node (or None if no path found)
    """
    start_time = time()
    queue = deque([start_node])
    visited = set([start_node])
    predecessor = {start_node: None}

    while queue:
        if time() - start_time > TRAVERSAL_TIMEOUT_SECONDS:
            raise TimeoutError("BFS timed out")
        if len(queue) > MAX_TRAVERSAL_QUEUE_SIZE:
            raise MemoryError("BFS queue size limit exceeded")

        current_node = queue.popleft()
        
        if debug or debug_bfs:
            print(f"Current Node: {current_node}")
            print(f"Queue State: {list(queue)}")
            print(f"Visited Nodes: {visited}")

        if current_node == end_node:
            return reconstruct_path(predecessor, start_node, end_node)
        
        for neighbor in graph[current_node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
                predecessor[neighbor] = current_node

    return None


def dfs(graph: Dict[str, List[str]], start_node: str, end_node: str, debug: bool = False, debug_dfs: bool = False) -> Optional[List[str]]:
    """
    Performs depth-first search (DFS) on the graph to find a path from
    start_node to end_node.

    :param graph: The graph represented as an adjacency list
    :param start_node: The start node for the DFS
    :param end_node: The end node for the DFS
    :param debug: A flag indicating whether to print general debug information
    :param debug_dfs: A flag indicating whether to print DFS specific debug information
    :return: A list representing the path from start_node to end_node (or None if no path found)
    """
    visited = set()
    predecessor = {}
    start_time = time()
    stack_size = 0

    def helper(current_node: str) -> bool:
        nonlocal stack_size
        if time() - start_time > TRAVERSAL_TIMEOUT_SECONDS:
            raise TimeoutError("DFS timed out")
        if stack_size > MAX_TRAVERSAL_QUEUE_SIZE:
            raise MemoryError("DFS stack size limit exceeded")
        
        if debug or debug_dfs:
            print(f"Current Node: {current_node}")
            print(f"Visited: {visited}")
        
        if current_node == end_node:
            return True
        visited.add(current_node)
        stack_size += 1
        
        for neighbor in graph[current_node]:
            if neighbor not in visited:
                predecessor[neighbor] = current_node
                if helper(neighbor):
                    return True
        
        stack_size -= 1
        return False

    if helper(start_node):
        return reconstruct_path(predecessor, start_node, end_node)
    else:
        return None


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


# Section: Main CLI Function
def graph_traversal_cli() -> None:
    """
    The main function that executes the command line interface for graph traversal.

    It gets user input, reads the graph from a file, and executes graph traversal algorithms.
    """
    while True:
        try:
            file_name = get_input(
                "Please enter the file name and extension (or type 'exit' to quit): "
            )
            if not file_name.endswith(CSV_FILE_EXTENSION):
                print(f"Invalid file extension. Please enter a valid {CSV_FILE_EXTENSION} file.")
                continue

            graph, error = read_graph_from_csv(file_name)
            if error:
                print(f"Error loading graph: {error}. Please check the file name and try again.")
                continue

            user_input_result = get_user_input(graph)
            start_node, end_node, graph, print_flag, debug_flag, visualize_flag, debug_bfs, debug_dfs = user_input_result

            if print_flag:
                print("Graph:")
                print_graph(graph)

            print("Loading file...")
            bfs_result = bfs(graph, start_node, end_node, debug=debug_flag, debug_bfs=debug_bfs)
            if bfs_result:
                print("Breadth-first traversal")
                print(" -> ".join(map(str, bfs_result)))
                if visualize_flag:
                    visualize_graph(graph, bfs_result)
            else:
                print("No path found in breadth-first traversal")

            dfs_result = dfs(graph, start_node, end_node, debug=debug_flag, debug_dfs=debug_dfs)
            if dfs_result:
                print("Depth-first Search")
                print(" -> ".join(map(str, dfs_result)))
                if visualize_flag:
                    visualize_graph(graph, dfs_result)
            else:
                print("No path found in depth-first search")

            break
        except SystemExit:
            print("Exiting...")
            exit()
        except Exception as e:
            print(f"An error occurred: {e}")
            break


# Run the main function
if __name__ == "__main__":
    graph_traversal_cli()
