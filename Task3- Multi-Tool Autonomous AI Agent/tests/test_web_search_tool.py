"""
Unit tests for the Web Search Tool.
"""

import unittest
from tools.web_search_tool import WebSearchTool


class TestWebSearchTool(unittest.TestCase):
    def setUp(self):
        self.tool = WebSearchTool()

    def test_search_execution(self):
        result = self.tool.run("Python programming language")
        self.assertIsNotNone(result)
        self.assertTrue(len(result) > 20)

    def test_empty_query_handled_safely(self):
        result = self.tool.run("   ")
        self.assertIsNotNone(result)


if __name__ == "__main__":
    unittest.main()
