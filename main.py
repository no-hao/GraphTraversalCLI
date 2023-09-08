from constants import CSV_FILE_EXTENSION
from input_output_utilities import read_graph_from_csv, get_input
from user_input_handling import get_user_input
from graph_traversal_algorithms import bfs, dfs
from visualization_and_printing import print_graph, visualize_graph


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
