import csv
from typing import Dict, List, Tuple, Optional

from constants import EXIT_COMMAND


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
