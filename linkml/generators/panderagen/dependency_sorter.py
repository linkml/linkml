class DependencySorter:
    """
    Module for sorting objects based on their dependencies.
    """

    def __init__(self, dependency_dict: dict[str, list[str]] = None):
        self.dependency_dict = dependency_dict or {}

    def expand_dependencies(self) -> None:
        """
        Expand dependencies to include all dependencies of the dependencies.
        """
        all_deps = set()

        for deps in self.dependency_dict.values():
            for dep in deps:
                all_deps.add(dep)

        for dep in all_deps:
            if dep not in self.dependency_dict:
                self.dependency_dict[dep] = []

    def sort_dependencies(self) -> list[str]:
        """
        Sort objects based on their dependencies.

        Returns:
            List of objects in order they should be declared

        Raises:
            ValueError: If there are cyclic dependencies
        """
        # Ensure all nodes have entries in the dictionary, even if empty
        self.expand_dependencies()

        result = []
        visited = set()
        temp_visited = set()

        def visit(node: str):
            if node in temp_visited:
                cycle_path = " -> ".join(list(temp_visited) + [node])
                raise ValueError(f"Cyclic dependency detected: {cycle_path}")

            if node not in visited:
                temp_visited.add(node)

                # Process dependencies if they exist
                for dependency in self.dependency_dict[node]:
                    if dependency in self.dependency_dict:  # Only process nodes that exist in the dict
                        visit(dependency)

                temp_visited.remove(node)
                visited.add(node)
                result.append(node)

        # Visit all nodes
        for node in self.dependency_dict:
            if node not in visited:
                visit(node)

        # Reverse to get correct declaration order (dependencies first)
        return result  # list(reversed(result))

    def add_dependency(self, node: str, dependency: str = None):
        """
        Add a single dependency to the dependency dictionary.
        If dependency is not provided or is None the node is added with an empty
        dependency list.

        Args:
            node: The node to which the dependency is added.
            dependency: The dependency to be added.
        """
        if node not in self.dependency_dict:
            self.dependency_dict[node] = []

        if dependency is not None and dependency not in self.dependency_dict[node]:
            self.dependency_dict[node].append(dependency)
