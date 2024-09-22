import os
from setuptools import setup, find_packages


def read_requirements(filename, base_path=".", seen_files=None):
    """Recursively read requirements from a file, processing '-r' lines."""
    if seen_files is None:
        seen_files = set()
    requirements = []
    filepath = os.path.join(base_path, filename)
    filepath = os.path.abspath(filepath)
    if filepath in seen_files:
        return []
    seen_files.add(filepath)
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("-r "):
                nested_filename = line[3:].strip()
                requirements.extend(
                    read_requirements(
                        nested_filename, os.path.dirname(filepath), seen_files
                    )
                )
            else:
                requirements.append(line)
    return requirements


# Read production dependencies
install_requires = read_requirements("requirements.txt")

# Read development dependencies
# (includes production dependencies via '-r requirements.txt')
dev_requirements = read_requirements("requirements-dev.txt")

# Remove duplicates from dev_requirements
dev_only_requirements = [req for req in dev_requirements if req not in install_requires]

extras_require = {
    "dev": dev_only_requirements,
}

# Read long description
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="dep_resolver",
    version="0.1.0",
    author="Konrad Kotlicki",
    description="Python dependency resolver.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/KKotlicki/dep_resolver",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=install_requires,
    extras_require=extras_require,
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "dep-resolver=dep_resolver.cli:run",
        ],
    },
)
