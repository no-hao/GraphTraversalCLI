# Graph Traversal Tool

## Overview

This tool allows users to load a graph structure from a CSV file and then perform graph traversal operations, specifically Breadth-First Search (BFS) and Depth-First Search (DFS), to find a path between two nodes in the graph. Additionally, it offers options for visualizing the graph and the paths found, and for printing debug information.

## Features

- **Graph Loading**: Loads a graph from a CSV file and represents it as an adjacency list.
- **User Input**: Prompts the user for necessary inputs including start and end nodes, and various operational flags.
- **Graph Traversal**: Implements BFS and DFS algorithms to find paths between two nodes in the graph.
- **Graph Visualization**: Visualizes the graph and the paths found using the NetworkX and Matplotlib libraries (optional).
- **Debugging Information**: Provides an option to print debug information during traversal (optional).
- **Graph Printing**: Prints the graph structure to the console (optional).

## Installation

Before running the script, ensure you have Python installed on your system. You may also need to install the `networkx` and `matplotlib` modules for graph visualization. These modules can be installed directly through the script when you choose the visualization option, or manually using the following commands:

```bash
pip install networkx matplotlib
```

## Usage

1. **Data Preparation**: Place your graph data in a CSV file with the following format:
   ```
   node_id,neighbor1_id,neighbor2_id,...
   ```
   Each row represents a node and its neighbors in the graph.
   
2. **Script Execution**: Run the script in a terminal or an IDE.

3. **User Input**: Follow the on-screen prompts to provide the necessary inputs:
   - CSV file name and extension
   - Start node ID
   - End node ID
   - Flags for printing the graph, enabling debug mode, and visualizing the graph

## Function Descriptions

### `read_graph_from_csv(file_path)`
Reads the graph data from the specified CSV file and returns it as an adjacency list.

### `get_user_input()`
Prompts the user to input necessary information for graph traversal.

### `bfs(graph, start_node, end_node, debug=False)`
Performs BFS on the graph to find the shortest path from `start_node` to `end_node`.

### `dfs(graph, start_node, end_node, debug=False)`
Performs DFS on the graph to find a path from `start_node` to `end_node`.

### `print_graph(graph)`
Prints the graph represented as an adjacency list.

### `visualize_graph(graph, path)`
Visualizes the graph and the specified path using NetworkX and Matplotlib.

### `main()`
The main function that orchestrates the entire process of reading the graph data from a file, getting user input, and performing BFS and DFS.

## Contribution

If you would like to contribute to this project, feel free to fork the repository and submit a pull request.

## License

[MIT License](LICENSE)

## Contact

For any queries or suggestions, please contact [es8070@ship.edu].

