import csv
from collections import deque

# Check if the necessary modules are installed
try:
    import networkx as nx
    import matplotlib.pyplot as plt
    visualization_modules_installed = True
except ImportError:
    visualization_modules_installed = False


def read_graph_from_csv(file_path):
    """
    Reads the graph data from the specified CSV file and returns it as an adjacency list.
    
    :param file_path: Path to the CSV file containing graph data
    :return: A tuple where the first element is an adjacency list (or None in case of error) and 
             the second element is an error message (or None if successful)
    """
    adjacency_list = {}
    try:
        with open(file_path, 'r', encoding='utf-8-sig') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                node = int(row[0])
                neighbors = set(map(int, filter(bool, row[1:])))
                adjacency_list[node] = neighbors
        return adjacency_list, None
    except Exception as e:
        return None, str(e)


def get_user_input():
    """
    Prompts the user to input necessary information for graph traversal, including the file path,
    start node, end node, and various flags for printing and visualization.
    
    :return: A tuple containing the file name, start node, end node, graph, and flags entered by the user
    """
    while True:
        file_name = input("Please enter the file name and extension: ")
        if not file_name.endswith('.csv'):
            print("Invalid file extension. Please enter a valid .csv file.")
            continue

        graph, error = read_graph_from_csv(file_name)
        if error:
            print(f"Error loading graph: {error}. "
                  "Please check the file name and try again.")
            continue

        start_node = input("Start node: ")
        end_node = input("End Node: ")
        print_flag = input("Enter p to print the graph, "
                           "or press Enter to continue: ")
        debug_flag = input("Enter d to enable debug mode (verbose output), "
                           "or press Enter to continue: ")
        visualize_flag = input("Enter v to visualize the graph and the "
                               "path found, or press Enter to continue: ")

        try:
            start_node = int(start_node)
            end_node = int(end_node)
            if start_node not in graph or end_node not in graph:
                raise ValueError("Node ID out of range")
            return file_name, start_node, end_node, graph, print_flag == 'p', debug_flag == 'd', visualize_flag == 'v'
        except ValueError as e:
            print(f"Invalid input: {e}. Please try again.")


def bfs(graph, start_node, end_node, debug=False):
    """
    Performs breadth-first search (BFS) on the graph to find the shortest path from start_node to end_node.
    
    :param graph: The graph represented as an adjacency list
    :param start_node: The start node for the BFS
    :param end_node: The end node for the BFS
    :param debug: A flag indicating whether to print debug information
    :return: A list representing the path from start_node to end_node (or None if no path found)
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
            path = []
            while current_node is not None:
                path.insert(0, current_node)
                current_node = predecessor[current_node]
            return path
        for neighbor in graph[current_node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
                predecessor[neighbor] = current_node
    return None


def dfs(graph, start_node, end_node, debug=False):
    """
    Performs depth-first search (DFS) on the graph to find a path from start_node to end_node.
    
    :param graph: The graph represented as an adjacency list
    :param start_node: The start node for the DFS
    :param end_node: The end node for the DFS
    :param debug: A flag indicating whether to print debug information
    :return: A list representing the path from start_node to end_node (or None if no path found)
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
            if neighbor not in visited and helper(neighbor):
                predecessor[neighbor] = current_node
                return True
        return False

    if helper(start_node):
        path = []
        current_node = end_node
        while current_node is not None:
            path.insert(0, current_node)
            current_node = predecessor.get(current_node)
        return path
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
        install_prompt = input("Do you want to install them now? (y/n): ").strip().lower()
        if install_prompt == 'y':
            import subprocess
            subprocess.check_call([sys.executable, "-m", "pip", "install", "networkx", "matplotlib"])
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
        nx.draw_networkx_edges(G, pos, edgelist=edges_in_path, edge_color='r', width=2, arrows=True)
        nx.draw_networkx_nodes(G, pos, nodelist=path, node_color='r')
    
    plt.show()


def main():
    """
    The main function that orchestrates the entire process of reading the graph data from a file,
    getting user input, and performing BFS and DFS.
    """
    while True:
        try:
            file_name, start_node, end_node, graph, print_flag, debug_flag, visualize_flag = get_user_input()

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
                    visualize_graph
                    visualize_graph(graph, dfs_result)
            else:
                print("No path found in depth-first search")

            break
        except Exception as e:
            print(f"An error occurred: {e}")
            break


# Run the main function
if __name__ == "__main__":
    main()
