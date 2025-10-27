class DependencySorter:
    """
    Module for sorting a dependency graph using string labels for nodes.
    This isolates the algorithm from other implementation details.
    The current implementation is intended as a helper for the LinkML Pandera generator
    rather than for general use.
    """

    def __init__(self, dependency_dict: dict[str, list[str]] = None):
        """
        Initialize the DependencySorter with a dictionary representing a dependency graph.

        :param dependency_dict: A dictionary where keys are labels and values are lists of dependency.
        :type dependency_dict: dict[str, list[str]], optional
        """
        self.dependency_dict = dependency_dict or {}

    def _expand_dependencies(self) -> None:
        """
        Explicitly represent nodes with no dependencies as having an empty dependency list.
        This is for easier lookup when visiting nodes.
        """
        nodes_with_dependencies = set(self.dependency_dict.keys())
        all_nodes = set(sum(self.dependency_dict.values(), []))
        no_dependency_nodes = all_nodes - nodes_with_dependencies
        leaf_dependency_graph = {n: [] for n in no_dependency_nodes}
        self.dependency_dict.update(leaf_dependency_graph)

    def _visit(self, node: str, visited: set[str], result: list[str]):
        """
        recursively visit dependencies in depth first order

        :param visited: tracks progress (initialize to set())
        :param result: builds sorted dependency list (initialize to [])
        """
        temp_visited = set()

        if node in temp_visited:
            cycle_path = " -> ".join(list(temp_visited) + [node])
            raise ValueError(f"Cyclic dependency detected: {cycle_path}")

        if node not in visited:
            temp_visited.add(node)

            for dependency in self.dependency_dict[node]:
                if dependency in self.dependency_dict:
                    self._visit(dependency, visited, result)

            temp_visited.remove(node)
            visited.add(node)
            result.append(node)

    def sort_dependencies(self) -> list[str]:
        """
        calculate the order of a dependency graph.

        :return: list of node label strings in dependency order.
        :raises ValueError: If there are cyclic dependencies
        """
        self._expand_dependencies()

        result = []
        visited = set()

        for node in self.dependency_dict:
            if node not in visited:
                self._visit(node, visited, result)

        return result

    def add_dependency(self, node: str, dependency: str = None):
        """
        Add a single dependency to the dependency dictionary.
        If dependency is not provided or is None the node is added with an empty
        dependency list.

        :param node: The node label to which the dependency is added.
        :param dependency: The dependency label to be added.
        """
        if node not in self.dependency_dict:
            self.dependency_dict[node] = []

        if dependency is not None and dependency not in self.dependency_dict[node]:
            self.dependency_dict[node].append(dependency)
