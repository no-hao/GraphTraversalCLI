from typing import Dict, List, Tuple

from input_output_utilities import get_input


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

