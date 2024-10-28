import unittest
from npm_registry import fetch_package_info
from unittest.mock import patch
from graph_generator import build_dependency_graph, generate_graphviz
import sys
from io import StringIO
from utils import parse_arguments

class TestNpmRegistry(unittest.TestCase):
    def test_fetch_package_info_valid(self):
        package_name = "express"
        try:
            package_info = fetch_package_info(package_name)
            self.assertEqual(package_info.get("name"), package_name)
        except Exception as e:
            self.fail(f"fetch_package_info raised an exception {e} for a valid package.")

    def test_fetch_package_info_invalid(self):
        package_name = "nonexistent-package-xyz123"
        with self.assertRaises(Exception) as context:
            fetch_package_info(package_name)
        self.assertIn("Failed to fetch package info", str(context.exception))


class TestGraphGenerator(unittest.TestCase):
    @patch('graph_generator.fetch_package_info')
    def test_build_dependency_graph(self, mock_fetch):
        mock_fetch.side_effect = [
            { 
                'dist-tags': {'latest': '4.17.1'},
                'versions': {
                    '4.17.1': {
                        'dependencies': {
                            'body-parser': '^1.19.0',
                            'cookie-parser': '^1.4.5'
                        }
                    }
                }
            },
            {  
                'dist-tags': {'latest': '1.19.0'},
                'versions': {
                    '1.19.0': {
                        'dependencies': {}
                    }
                }
            },
            {  
                'dist-tags': {'latest': '1.4.5'},
                'versions': {
                    '1.4.5': {
                        'dependencies': {}
                    }
                }
            }
        ]

        graph = build_dependency_graph('express', max_depth=1)
        expected_graph = {
            'express': ['body-parser', 'cookie-parser'],
            'body-parser': [],
            'cookie-parser': []
        }
        self.assertEqual(graph, expected_graph)

    def test_generate_graphviz(self):
        sample_graph = {
            'express': ['body-parser', 'cookie-parser'],
            'body-parser': [],
            'cookie-parser': []
        }
        expected_output = """digraph G {
    "express" -> "body-parser";
    "express" -> "cookie-parser";
}"""
        graphviz_code = generate_graphviz(sample_graph)
        self.assertEqual(graphviz_code.strip(), expected_output.strip())


class TestUtils(unittest.TestCase):
    @patch('sys.exit')
    @patch('os.path.isfile')
    @patch('os.access')
    def test_parse_arguments_valid(self, mock_access, mock_isfile, mock_exit):
        test_args = [
            'program',
            '/usr/local/bin/dot',
            'express',
            './express.dot',
            '2',
            'https://github.com/expressjs/express'
        ]
        mock_isfile.return_value = True
        mock_access.return_value = True

        with patch.object(sys, 'argv', test_args):
            args = parse_arguments()
            self.assertEqual(args.graph_path, '/usr/local/bin/dot')
            self.assertEqual(args.package_name, 'express')
            self.assertEqual(args.result_file_path, './express.dot')
            self.assertEqual(args.max_depth, 2)
            self.assertEqual(args.repository_url, 'https://github.com/expressjs/express')
            mock_exit.assert_not_called()

    @patch('sys.exit')
    @patch('os.path.isfile')
    @patch('os.access')
    def test_parse_arguments_invalid_dot_path(self, mock_access, mock_isfile, mock_exit):
        test_args = [
            'program',
            '/invalid/path/dot',
            'express',
            './express.dot',
            '2',
            'https://github.com/expressjs/express'
        ]
        mock_isfile.return_value = False
        mock_access.return_value = False

        with patch.object(sys, 'argv', test_args), patch('builtins.print') as mock_print:
            parse_arguments()
            mock_print.assert_called_with("Error: The graph visualization program '/invalid/path/dot' is not executable or does not exist.")
            mock_exit.assert_called_with(1)

    @patch('sys.exit')
    @patch('os.path.isfile')
    @patch('os.access')
    def test_parse_arguments_invalid_max_depth(self, mock_access, mock_isfile, mock_exit):
        """Test parsing with invalid max depth."""
        test_args = [
            'program',
            '/usr/local/bin/dot',
            'express',
            './express.dot',
            '-1',
            'https://github.com/expressjs/express'
        ]
        mock_isfile.return_value = True
        mock_access.return_value = True

        with patch.object(sys, 'argv', test_args), patch('builtins.print') as mock_print:
            parse_arguments()
            mock_print.assert_called_with("Error: Maximum depth must be a non-negative integer.")
            mock_exit.assert_called_with(1)

if __name__ == "__main__":
    unittest.main()