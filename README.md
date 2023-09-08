# Graph Traversal Tool

## Overview

This tool allows users to load a graph structure from a CSV file and then perform graph traversal operations, specifically Breadth-First Search (BFS) and Depth-First Search (DFS), to find a path between two nodes in the graph. Additionally, it offers options for visualizing the graph and the paths found, and for printing debug information.

## Features

- **Graph Loading**: Loads a graph from a CSV file and represents it as an adjacency list.
- **User Input**: Prompts the user for necessary inputs including start and end nodes, and various operational flags. Users can exit at any prompt by typing 'exit'.
- **Graph Traversal**: Implements BFS and DFS algorithms to find paths between two nodes in the graph.
- **Graph Visualization**: Visualizes the graph and the paths found using the NetworkX and Matplotlib libraries (optional).
- **Debugging Information**: Provides an option to print debug information during traversal (optional).
- **Graph Printing**: Prints the graph structure to the console (optional).
- **Exit Command**: Allows users to exit the script at any time by entering the 'exit' command.

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

### File Structure

Your project should have the following structure:

```
project_folder/
│
├── constants.py                   # File containing constant values
├── input_output_utilities.py      # File with functions for input and output operations
├── user_input_handling.py         # File for handling user inputs
├── graph_traversal_algorithms.py  # File implementing the BFS and DFS algorithms
├── visualization_and_printing.py  # File for graph visualization and printing
└── main.py                        # Main script to run the tool
```

### Function Descriptions

- `constants.py`: Holds the constants used across the script.
- `input_output_utilities.py`: Contains functions for reading the graph from a CSV file and getting user inputs.
- `user_input_handling.py`: Includes functions for handling and validating user inputs.
- `graph_traversal_algorithms.py`: Contains the BFS and DFS algorithms and a function for path reconstruction.
- `graph_visualization_and_printing.py`: Houses functions for printing the graph to the console and visualizing the graph using NetworkX and Matplotlib.
- `main.py`: The main script that integrates all the other modules and runs the command line interface for the graph traversal tool.

To run the tool, execute the `main.py` script.

## Contribution

If you would like to contribute to this project, feel free to fork the repository and submit a pull request.

## License

[MIT License](LICENSE)

## Contact

For any queries or suggestions, please contact [es8070@ship.edu].
