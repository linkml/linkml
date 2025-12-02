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
        nodes_with_dependencies = set(self.dependency_dict)
        all_nodes = set(sum(self.dependency_dict.values(), []))
        no_dependency_nodes = all_nodes - nodes_with_dependencies
        leaf_dependency_graph = {n: [] for n in no_dependency_nodes}
        self.dependency_dict.update(leaf_dependency_graph)

    def _visit(self, node: str, visited: set[str], in_progress: set[str], result: list[str]) -> None:
        """
        recursively visit dependencies in depth first order.
        the graph dicts are assumed to be in proper form (aside from cycles)

        :param visited: tracks progress (initialize to set())
        :param result: builds sorted dependency list (initialize to [])
        :param in_progress: for tracking cycles (initialize to set())
        """
        if node in visited:
            return
        if node in in_progress:
            cycle_path = " -> ".join(list(in_progress) + [node])

            raise ValueError(f"Cyclic dependency detected: {cycle_path}")

        in_progress.add(node)
        for dependency in self.dependency_dict[node]:
            self._visit(dependency, visited, in_progress, result)
        in_progress.remove(node)
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
        in_progress = set()

        for node in self.dependency_dict:
            if node not in visited:
                self._visit(node, visited, in_progress, result)

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
