import os
import pathspec


def load_gitignore(gitignore_path=".gitignore", allowed_entries=None):
    """Load ignore patterns from .gitignore file if it exists, and add exceptions."""
    if allowed_entries is None:
        allowed_entries = []
    patterns = []
    if os.path.exists(gitignore_path):
        with open(gitignore_path, "r") as f:
            patterns = f.read().splitlines()
    # Add exceptions for allowed entries
    for entry in allowed_entries:
        patterns.append(f"!{entry}")
    return patterns


def generate_tree(start_path=".", ignore_patterns_list=None):
    """Generate directory tree, ignoring files and directories based on patterns."""
    tree = []
    if ignore_patterns_list is None:
        ignore_patterns_list = []

    # Append extra ignore patterns
    extra_ignore_patterns = [
        "_static",
        "_templates",
        "__pycache__",
        "htmlcov",
        "dep_resolver.egg-info",
        "venv",
        "build",
    ]
    ignore_patterns_list.extend(extra_ignore_patterns)

    # Create pathspec object for matching ignore patterns using 'gitignore' syntax
    ignore_spec = pathspec.PathSpec.from_lines("gitignore", ignore_patterns_list)

    root_dir_name = os.path.basename(os.path.abspath(start_path))
    tree.append(root_dir_name + "/")

    def inner(dir_path, prefix=""):
        try:
            contents = os.listdir(dir_path)
        except PermissionError:
            return

        # Exclude hidden files and directories unless they are allowed entries
        contents = [
            entry
            for entry in contents
            if not entry.startswith(".") or entry in allowed_entries
        ]

        # Separate directories and files
        dirs = [d for d in contents if os.path.isdir(os.path.join(dir_path, d))]
        files = [f for f in contents if os.path.isfile(os.path.join(dir_path, f))]

        # Prepare relative paths for matching
        rel_paths_dirs = [
            os.path.relpath(os.path.join(dir_path, d), start_path) + "/" for d in dirs
        ]
        rel_paths_files = [
            os.path.relpath(os.path.join(dir_path, f), start_path) for f in files
        ]

        # Normalize file paths
        rel_paths_dirs = [os.path.normpath(path) for path in rel_paths_dirs]
        rel_paths_files = [os.path.normpath(path) for path in rel_paths_files]

        # Filter out ignored directories
        dirs = [
            d
            for d, rel_path in zip(dirs, rel_paths_dirs)
            if not ignore_spec.match_file(rel_path)
        ]

        # Filter out ignored files
        files = [
            f
            for f, rel_path in zip(files, rel_paths_files)
            if not ignore_spec.match_file(rel_path)
        ]

        # Sort directories and files alphabetically
        dirs.sort()
        files.sort()

        # Prepare pointers
        entries = dirs + files
        if entries:
            pointers = ["├── "] * (len(entries) - 1) + ["└── "]
        else:
            pointers = []

        # Process directories
        for i, directory in enumerate(dirs):
            path = os.path.join(dir_path, directory)

            # Skip contents of 'test_data/', but include the directory itself
            if directory == "test_data":
                tree.append(prefix + pointers[i] + directory + "/")
                continue

            tree.append(prefix + pointers[i] + directory + "/")
            extension = "│   " if pointers[i] == "├── " else "    "
            inner(path, prefix + extension)

        # Process files
        for i, filename in enumerate(files):
            idx = len(dirs) + i
            tree.append(prefix + pointers[idx] + filename)

    inner(start_path)
    return "\n".join(tree)


def update_readme(tree_str):
    """Update the README.md file with the generated directory tree."""
    with open("README.md", "r") as f:
        content = f.read()

    start_marker = "<!-- PROJECT STRUCTURE START -->"
    end_marker = "<!-- PROJECT STRUCTURE END -->"

    new_content = (
        content.split(start_marker)[0]
        + start_marker
        + "\n\n```plaintext\n"
        + tree_str
        + "\n```\n\n"
        + end_marker
        + content.split(end_marker)[1]
    )

    with open("README.md", "w") as f:
        f.write(new_content)


if __name__ == "__main__":
    # Define allowed entries
    allowed_entries = [".gitignore", ".github", ".pre-commit-config.yaml"]
    # Load .gitignore patterns with exceptions
    ignore_patterns_list = load_gitignore(allowed_entries=allowed_entries)
    # Generate the directory tree
    tree = generate_tree(".", ignore_patterns_list)
    # Update README.md with the tree structure
    update_readme(tree)
