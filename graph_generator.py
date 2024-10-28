from npm_registry import fetch_package_info

def build_dependency_graph(package_name, max_depth, current_depth=0, graph=None, visited=None):
    if graph is None:
        graph = {}
    if visited is None:
        visited = set()

    if current_depth > max_depth or package_name in visited:
        return

    visited.add(package_name)

    try:
        package_info = fetch_package_info(package_name)
        latest_version = package_info.get('dist-tags', {}).get('latest')
        dependencies = package_info.get('versions', {}).get(latest_version, {}).get('dependencies', {})
        dependency_names = list(dependencies.keys())
        graph[package_name] = dependency_names

        for dep in dependency_names:
            build_dependency_graph(dep, max_depth, current_depth + 1, graph, visited)
    except Exception as e:
        print(f"Warning: {e}")

    return graph

def generate_graphviz(graph):
    lines = ["digraph G {"]
    for pkg, deps in graph.items():
        for dep in deps:
            lines.append(f'    "{pkg}" -> "{dep}";')
    lines.append("}")
    return "\n".join(lines)