"""
Unit tests for the File Reader Tool.
"""

import unittest
from pathlib import Path
from tools.file_reader_tool import FileReaderTool


class TestFileReaderTool(unittest.TestCase):
    def setUp(self):
        self.tool = FileReaderTool()

    def test_read_json_file(self):
        result = self.tool.run("workspace_data/enterprise_budget_2025.json")
        self.assertIn("fiscal_year", result)
        self.assertIn("Datheon AI Technologies", result)
        self.assertIn("allocated_budget", result)

    def test_read_txt_file(self):
        result = self.tool.run("workspace_data/cloud_cost_breakdown.txt")
        self.assertIn("Datheon Cloud Cost Analysis", result)
        self.assertIn("$95,000", result)

    def test_list_directory(self):
        result = self.tool.run("list:workspace_data")
        self.assertIn("enterprise_budget_2025.json", result)
        self.assertIn("cloud_cost_breakdown.txt", result)

    def test_nonexistent_file(self):
        result = self.tool.run("nonexistent_path/fake_file.json")
        self.assertIn("Error: File not found", result)


if __name__ == "__main__":
    unittest.main()
