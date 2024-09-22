import unittest
from dep_resolver.printer import print_dependency_graph
from io import StringIO
from unittest.mock import patch


class TestPrinter(unittest.TestCase):
    def test_print_dependency_graph(self):
        resolved_graph = {
            "pkg1": {"pkg2": {"pkg3": {}}, "pkg3": {}},
            "pkg2": {"pkg3": {}},
            "pkg3": {},
        }
        expected_output = (
            "- pkg1\n"
            "    - pkg2\n"
            "        - pkg3\n"
            "    - pkg3\n"
            "- pkg2\n"
            "    - pkg3\n"
            "- pkg3\n"
        )
        with patch("sys.stdout", new=StringIO()) as fake_out:
            print_dependency_graph(resolved_graph)
            self.assertEqual(fake_out.getvalue(), expected_output)


if __name__ == "__main__":
    unittest.main()
