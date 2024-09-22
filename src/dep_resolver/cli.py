import argparse
import json
import logging
from pathlib import Path
from dep_resolver.resolver import resolve_dependencies
from dep_resolver.printer import print_dependency_graph


def run() -> int:
    parser = argparse.ArgumentParser(description="Dependency Resolver")
    parser.add_argument("json_file", type=Path, help="Path to the JSON file")
    parser.add_argument(
        "--log-level",
        type=str,
        default="WARNING",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Set the logging level",
    )
    parser.add_argument(
        "--indent-size", default=4, type=int, help="Set the indentation size for output"
    )
    args = parser.parse_args()

    # Set up logging
    numeric_level = getattr(logging, args.log_level.upper(), None)
    logging.basicConfig(level=numeric_level, format="%(levelname)s:%(message)s")
    logger = logging.getLogger(__name__)

    json_file = args.json_file
    if not json_file.is_file():
        logger.error(f"File not found: {json_file}")
        return 1

    try:
        with json_file.open("r") as f:
            dependencies = json.load(f)
            logger.debug(f"Loaded dependencies: {dependencies}")
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON file: {e}")
        return 1
    except Exception as e:
        logger.error(f"An unexpected error occurred while reading the file: {e}")
        return 1

    try:
        resolved_graph = resolve_dependencies(dependencies)
    except RecursionError as e:
        logger.error(f"An error occurred while resolving dependencies: {e}")
        return 1
    except Exception as e:
        logger.error(f"An unexpected error occurred during dependency resolution: {e}")
        return 1

    try:
        print_dependency_graph(resolved_graph, indent_size=args.indent_size)
    except Exception as e:
        logger.error(
            f"An unexpected error occurred while printing the dependency graph: {e}"
        )
        return 1
    return 0
