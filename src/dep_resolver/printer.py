from __future__ import annotations
from typing import Dict

DependencyGraph = Dict[str, "DependencyGraph"]


def print_dependency_graph(
    resolved_graph: DependencyGraph, indent_size: int = 4
) -> None:
    """
    Prints the resolved dependency graph.

    Args:
        resolved_graph (DependencyGraph): The resolved dependency graph.
        indent_size (int): Number of spaces for indentation.
    """
    for pkg in resolved_graph:
        _print_tree(pkg, resolved_graph[pkg], indent=0, indent_size=indent_size)


def _print_tree(
    pkg: str, sub_deps: DependencyGraph, indent: int, indent_size: int
) -> None:
    """
    Recursively prints the dependency tree.

    Args:
        pkg (str): Package name.
        sub_deps (DependencyGraph): Sub-dependencies.
        indent (int): Current indentation level.
        indent_size (int): Number of spaces for indentation.
    """
    print(" " * indent_size * indent + "- " + pkg)
    for sub_pkg in sub_deps:
        _print_tree(sub_pkg, sub_deps[sub_pkg], indent + 1, indent_size)
