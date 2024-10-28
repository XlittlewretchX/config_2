import sys
import os
import subprocess
from graph_generator import build_dependency_graph, generate_graphviz
from utils import parse_arguments

def main():
    args = parse_arguments()

    graph_path = args.graph_path
    package_name = args.package_name
    result_file_path = args.result_file_path
    max_depth = args.max_depth
    repository_url = args.repository_url

    print(f"Analyzing package: {package_name}")
    print(f"Fetching dependencies up to depth: {max_depth}\n")

    graph = build_dependency_graph(package_name, max_depth)
    graphviz_code = generate_graphviz(graph)

    try:
        with open(result_file_path, 'w') as file:
            file.write(graphviz_code)
        print(f"Graphviz code written to '{result_file_path}'")
    except IOError as e:
        print(f"Error writing to file '{result_file_path}': {str(e)}")
        sys.exit(1)

    print("\nGraphviz Representation:\n")
    print(graphviz_code)

    
if __name__ == "__main__":
    main()