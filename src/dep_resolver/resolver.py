from __future__ import annotations
from typing import Dict, List, Set
import logging

logger = logging.getLogger(__name__)

DependencyGraph = Dict[str, "DependencyGraph"]


def resolve_dependencies(dependencies: Dict[str, List[str]]) -> DependencyGraph:
    """
    Resolves the full dependency graph.

    Args:
        dependencies (Dict[str, List[str]]): The initial dependency mapping.

    Returns:
        DependencyGraph: The resolved dependency graph.

    Raises:
        RecursionError: If a circular dependency is detected.
    """
    resolved = {}
    for pkg in dependencies:
        visited: Set[str] = set()
        logger.info(f"Resolving dependencies for package: {pkg}")
        resolved[pkg] = _resolve_pkg(pkg, dependencies, visited)
    return resolved


def _resolve_pkg(
    pkg: str, dependencies: Dict[str, List[str]], visited: Set[str]
) -> DependencyGraph:
    """
    Helper function to recursively resolve dependencies.

    Args:
        pkg (str): The package name.
        dependencies (Dict[str, List[str]]): The dependency mapping.
        visited (Set[str]): Set of visited packages to detect cycles.

    Returns:
        DependencyGraph: Resolved dependencies for the package.
    """
    if pkg in visited:
        raise RecursionError(f"Circular dependency detected: {pkg} already visited")
    visited.add(pkg)
    logger.debug(f"Visiting package: {pkg}")
    deps: DependencyGraph = {}
    for dep in dependencies.get(pkg, []):
        deps[dep] = _resolve_pkg(dep, dependencies, visited.copy())
    return deps
