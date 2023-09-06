import csv
from collections import deque

# Constants
EXIT_COMMAND = 'exit'
CSV_EXTENSION = '.csv'


def get_input(prompt):
    user_input = input(prompt)
    if user_input.lower() == EXIT_COMMAND:
        print("Exiting...")
        exit()
    return user_input


def read_graph_from_csv(file_path):
    """
    Reads the graph data from the specified CSV file and returns it as an
    adjacency list.
    :param file_path: Path to the CSV file containing graph data
    :return: A tuple where the first element is an adjacency list (or None in
             case of error) and the second element is an error message (or None
             if successful)
    """
    adjacency_list = {}
    try:
        with open(file_path, 'r', encoding='utf-8-sig') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                node = int(row[0])
                adjacency_list[node] = [int(neigh) for neigh in row[1:] if neigh]
        return adjacency_list, None
    except Exception as e:
        return None, str(e)


def get_user_input(graph):
    """
    Prompts the user to input necessary information for graph traversal,
    including the start node, end node, and various flags for printing and
    visualization.
    :param graph: The graph represented as an adjacency list
    :return: A tuple containing the start node, end node, graph, and flags
             entered by the user
    """
    while True:
        try:
            start_node = int(get_input("Start node (or type 'exit' to quit): "))
            end_node = int(get_input("End Node (or type 'exit' to quit): "))

            if start_node not in graph or end_node not in graph:
                raise ValueError("Node ID out of range")

            print_flag_input = get_input(
                "Enter p to print the graph, or type 'exit' to quit, or press "
                "Enter to continue: "
            )
            debug_flag_input = get_input(
                "Enter d to enable debug mode (verbose output), or type 'exit' "
                "to quit, or press Enter to continue: "
            )
            visualize_flag_input = get_input(
                "Enter v to visualize the graph and the path found, or type "
                "'exit' to quit, or press Enter to continue: "
            )

            return (
                start_node, end_node, graph,
                print_flag_input == 'p',
                debug_flag_input == 'd',
                visualize_flag_input == 'v'
            )
        except ValueError as e:
            print(f"Invalid input: {e}. Please try again.")
        except SystemExit:
            raise


def reconstruct_path(predecessor, start_node, end_node):
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

def bfs(graph, start_node, end_node, debug=False):
    """
    Performs breadth-first search (BFS) on the graph to find the shortest path
    from start_node to end_node.
    :param graph: The graph represented as an adjacency list
    :param start_node: The start node for the BFS
    :param end_node: The end node for the BFS
    :param debug: A flag indicating whether to print debug information
    :return: A list representing the path from start_node to end_node (or None
             if no path found)
    """
    queue = deque([start_node])
    visited = set([start_node])
    predecessor = {start_node: None}
    while queue:
        if debug:
            print(f"Queue: {queue}")
            print(f"Visited: {visited}")

        current_node = queue.popleft()
        if current_node == end_node:
            return reconstruct_path(predecessor, start_node, end_node)
        for neighbor in graph[current_node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
                predecessor[neighbor] = current_node
    return None

def dfs(graph, start_node, end_node, debug=False):
    """
    Performs depth-first search (DFS) on the graph to find a path from
    start_node to end_node.
    :param graph: The graph represented as an adjacency list
    :param start_node: The start node for the DFS
    :param end_node: The end node for the DFS
    :param debug: A flag indicating whether to print debug information
    :return: A list representing the path from start_node to end_node (or None
             if no path found)
    """
    visited = set()
    predecessor = {}

    def helper(current_node):
        if debug:
            print(f"Current Node: {current_node}")
            print(f"Visited: {visited}")

        if current_node == end_node:
            return True
        visited.add(current_node)
        for neighbor in graph[current_node]:
            if neighbor not in visited:
                predecessor[neighbor] = current_node  # Moved this line up
                if helper(neighbor):
                    return True
        return False

    if helper(start_node):
        return reconstruct_path(predecessor, start_node, end_node)
    else:
        return None


def print_graph(graph):
    """
    Prints the graph represented as an adjacency list.
    :param graph: The graph represented as an adjacency list
    """
    for node, neighbors in graph.items():
        neighbors_str = " -> ".join(map(str, neighbors))
        print(f"{node} -> {neighbors_str}")


def visualize_graph(graph, path):
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


def graph_traversal_cli():
    """
    The main function that orchestrates the entire process of reading the graph
    data from a file, getting user input, and performing BFS and DFS.
    """
    while True:
        try:
            file_name = get_input(
                "Please enter the file name and extension (or type 'exit' to quit): "
            )
            if not file_name.endswith(CSV_EXTENSION):
                print(f"Invalid file extension. Please enter a valid {CSV_EXTENSION} file.")
                continue

            graph, error = read_graph_from_csv(file_name)
            if error:
                print(f"Error loading graph: {error}. Please check the file name and try again.")
                continue

            user_input_result = get_user_input(graph)
            start_node, end_node, graph, print_flag, debug_flag, visualize_flag = user_input_result

            if print_flag:
                print("Graph:")
                print_graph(graph)

            print("Loading file...")
            bfs_result = bfs(graph, start_node, end_node, debug=debug_flag)
            if bfs_result:
                print("Breadth-first traversal")
                print(" -> ".join(map(str, bfs_result)))
                if visualize_flag:
                    visualize_graph(graph, bfs_result)
            else:
                print("No path found in breadth-first traversal")

            dfs_result = dfs(graph, start_node, end_node, debug=debug_flag)
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
