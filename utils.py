import argparse
import os
import sys

def parse_arguments():
    parser = argparse.ArgumentParser(description="Visualize npm package dependencies using Graphviz.")
    parser.add_argument("graph_path", help="Path to the Graphviz 'dot' executable.")
    parser.add_argument("package_name", help="Name of the npm package to analyze.")
    parser.add_argument("result_file_path", help="Path to the output DOT file.")
    parser.add_argument("max_depth", type=int, help="Maximum depth of dependency analysis.")
    parser.add_argument("repository_url", help="Repository URL of the package.")

    args = parser.parse_args()

    if not os.path.isfile(args.graph_path) or not os.access(args.graph_path, os.X_OK):
        print(f"Error: The graph visualization program '{args.graph_path}' is not executable or does not exist.")
        sys.exit(1)


    if args.max_depth < 0:
        print("Error: Maximum depth must be a non-negative integer.")
        sys.exit(1)

    return args