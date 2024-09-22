import unittest
from unittest.mock import patch, mock_open
from io import StringIO
from pathlib import Path
from dep_resolver.cli import run
import argparse


class TestCLI(unittest.TestCase):
    @patch("argparse.ArgumentParser.parse_args")
    def test_cli_file_not_found(self, mock_args):
        mock_args.return_value = argparse.Namespace(
            json_file=Path("nonexistent.json"), log_level="INFO", indent_size=4
        )
        with self.assertLogs("dep_resolver.cli", level="ERROR") as cm:
            exit_code = run()
            self.assertEqual(exit_code, 1)
            self.assertIn("File not found", cm.output[0])

    @patch("argparse.ArgumentParser.parse_args")
    def test_cli_invalid_json(self, mock_args):
        mock_args.return_value = argparse.Namespace(
            json_file=Path("tests/test_data/invalid.json"),
            log_level="INFO",
            indent_size=4,
        )
        with patch("builtins.open", mock_open(read_data='{"invalid_json": ')):
            with self.assertLogs("dep_resolver.cli", level="ERROR") as cm:
                exit_code = run()
                self.assertEqual(exit_code, 1)
                self.assertIn("Invalid JSON file", cm.output[0])

    @patch("argparse.ArgumentParser.parse_args")
    def test_cli_unexpected_exception(self, mock_args):
        mock_args.return_value = argparse.Namespace(
            json_file=Path("tests/test_data/dependencies.json"),
            log_level="INFO",
            indent_size=4,
        )
        with patch("json.load", side_effect=Exception("Unexpected error")):
            with self.assertLogs("dep_resolver.cli", level="ERROR") as cm:
                exit_code = run()
                self.assertEqual(exit_code, 1)
                self.assertIn(
                    "An unexpected error occurred while reading the file", cm.output[0]
                )

    @patch("argparse.ArgumentParser.parse_args")
    def test_cli_unexpected_resolution_exception(self, mock_args):
        mock_args.return_value = argparse.Namespace(
            json_file=Path("tests/test_data/dependencies.json"),
            log_level="INFO",
            indent_size=4,
        )
        with patch(
            "dep_resolver.cli.resolve_dependencies",
            side_effect=Exception("Unexpected error"),
        ):
            with self.assertLogs("dep_resolver.cli", level="ERROR") as cm:
                exit_code = run()
                self.assertEqual(exit_code, 1)
                self.assertIn(
                    "An unexpected error occurred during dependency resolution",
                    cm.output[0],
                )

    @patch("argparse.ArgumentParser.parse_args")
    def test_cli_print_exception(self, mock_args):
        mock_args.return_value = argparse.Namespace(
            json_file=Path("tests/test_data/dependencies.json"),
            log_level="INFO",
            indent_size=4,
        )
        with patch(
            "dep_resolver.cli.print_dependency_graph",
            side_effect=Exception("Print error"),
        ):
            with self.assertLogs("dep_resolver.cli", level="ERROR") as cm:
                exit_code = run()
                self.assertEqual(exit_code, 1)
                self.assertIn(
                    "An unexpected error occurred while printing the dependency graph",
                    cm.output[0],
                )

    @patch("argparse.ArgumentParser.parse_args")
    def test_cli_recursion_error(self, mock_args):
        mock_args.return_value = argparse.Namespace(
            json_file=Path("tests/test_data/circular.json"),
            log_level="INFO",
            indent_size=4,
        )
        with self.assertLogs("dep_resolver.cli", level="ERROR") as cm:
            exit_code = run()
            self.assertEqual(exit_code, 1)
            self.assertIn(
                "An error occurred while resolving dependencies", cm.output[0]
            )

    @patch("argparse.ArgumentParser.parse_args")
    def test_cli_success(self, mock_args):
        mock_args.return_value = argparse.Namespace(
            json_file=Path("tests/test_data/dependencies.json"),
            log_level="INFO",
            indent_size=4,
        )
        with patch("sys.stdout", new=StringIO()) as fake_out:
            exit_code = run()
            self.assertEqual(exit_code, 0)
            output = fake_out.getvalue()
            self.assertIn("- pkg1", output)


if __name__ == "__main__":
    unittest.main()
