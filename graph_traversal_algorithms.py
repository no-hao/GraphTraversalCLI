from collections import deque
from time import time
from typing import Dict, List, Optional

from constants import MAX_TRAVERSAL_QUEUE_SIZE, TRAVERSAL_TIMEOUT_SECONDS


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
    Performs breadth-first search (BFS) on the graph to find the shortest path from start_node to end_node.
    Now includes detailed debug information such as current level, queue size, and time elapsed.

    :param graph: The graph represented as an adjacency list
    :param start_node: The start node for the BFS
    :param end_node: The end node for the BFS
    :param debug: A flag indicating whether to print general debug information
    :param debug_bfs: A flag indicating whether to print BFS specific debug information
    :return: A list representing the path from start_node to end_node (or None if no path found)
    """
    start_time = time()
    queue = deque([(start_node, 0)])  # Include level information
    visited = set([start_node])
    predecessor = {start_node: None}

    while queue:
        if time() - start_time > TRAVERSAL_TIMEOUT_SECONDS:
            raise TimeoutError("BFS timed out")
        if len(queue) > MAX_TRAVERSAL_QUEUE_SIZE:
            raise MemoryError("BFS queue size limit exceeded")

        current_node, level = queue.popleft()

        if debug or debug_bfs:
            print(f"Current Node: {current_node}")
            print(f"Current Level: {level}")
            print(f"Queue Size: {len(queue)}")
            print(f"Time Elapsed: {time() - start_time:.2f} seconds")

        if current_node == end_node:
            return reconstruct_path(predecessor, start_node, end_node)
        
        for neighbor in graph[current_node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, level+1))
                predecessor[neighbor] = current_node

    return None


def dfs(graph: Dict[str, List[str]], start_node: str, end_node: str, debug: bool = False, debug_dfs: bool = False) -> Optional[List[str]]:
    """
    Performs depth-first search (DFS) on the graph to find a path from start_node to end_node.
    Now includes detailed debug information such as current recursion depth, stack size, and time elapsed,
    along with information on backtracking steps.

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

    def helper(current_node: str, depth: int) -> bool:
        nonlocal stack_size
        if time() - start_time > TRAVERSAL_TIMEOUT_SECONDS:
            raise TimeoutError("DFS timed out")
        if stack_size > MAX_TRAVERSAL_QUEUE_SIZE:
            raise MemoryError("DFS stack size limit exceeded")
        
        if debug or debug_dfs:
            print(f"Current Node: {current_node}")
            print(f"Current Recursion Depth: {depth}")
            print(f"Stack Size: {stack_size}")
            print(f"Time Elapsed: {time() - start_time:.2f} seconds")
        
        if current_node == end_node:
            return True
        visited.add(current_node)
        stack_size += 1
        
        for neighbor in graph[current_node]:
            if neighbor not in visited:
                predecessor[neighbor] = current_node
                if helper(neighbor, depth+1):
                    return True
        
        if debug or debug_dfs:
            print(f"Backtracking from: {current_node}")
        
        stack_size -= 1
        return False

    if helper(start_node, 0):
        return reconstruct_path(predecessor, start_node, end_node)
    else:
        return None
