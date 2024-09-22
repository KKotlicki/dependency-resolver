import unittest
from dep_resolver.resolver import resolve_dependencies


class TestDependencyResolver(unittest.TestCase):
    def test_resolve_dependencies(self):
        dependencies = {"pkg1": ["pkg2", "pkg3"], "pkg2": ["pkg3"], "pkg3": []}
        expected_output = {
            "pkg1": {"pkg2": {"pkg3": {}}, "pkg3": {}},
            "pkg2": {"pkg3": {}},
            "pkg3": {},
        }

        result = resolve_dependencies(dependencies)
        self.assertEqual(result, expected_output)

    def test_circular_dependency(self):
        dependencies = {"pkg1": ["pkg2"], "pkg2": ["pkg1"]}
        with self.assertRaises(RecursionError):
            resolve_dependencies(dependencies)

    def test_missing_dependency(self):
        dependencies = {
            "pkg1": ["pkg2"],
            "pkg2": ["pkg3"],
            # pkg3 is not defined
        }
        result = resolve_dependencies(dependencies)
        self.assertEqual(result, {"pkg1": {"pkg2": {"pkg3": {}}}, "pkg2": {"pkg3": {}}})

    def test_empty_dependencies(self):
        dependencies = {}
        expected_output = {}
        result = resolve_dependencies(dependencies)
        self.assertEqual(result, expected_output)

    def test_self_dependency(self):
        dependencies = {"pkg1": ["pkg1"]}
        with self.assertRaises(RecursionError):
            resolve_dependencies(dependencies)

    def test_nonexistent_dependency(self):
        dependencies = {
            "pkg1": ["pkg2"],
            "pkg2": ["pkg3"],
            "pkg3": ["pkg4"],
            # "pkg4" is not defined
        }
        expected_output = {
            "pkg1": {"pkg2": {"pkg3": {"pkg4": {}}}},
            "pkg2": {"pkg3": {"pkg4": {}}},
            "pkg3": {"pkg4": {}},
        }
        result = resolve_dependencies(dependencies)
        self.assertEqual(result, expected_output)

    def test_recursion_error_handling(self):
        dependencies = {"pkg1": ["pkg2"], "pkg2": ["pkg3"], "pkg3": ["pkg1"]}
        with self.assertRaises(RecursionError):
            resolve_dependencies(dependencies)

    def test_already_visited_package(self):
        dependencies = {"pkg1": ["pkg1"]}  # Self-dependency
        with self.assertRaises(RecursionError):
            resolve_dependencies(dependencies)


if __name__ == "__main__":
    unittest.main()
