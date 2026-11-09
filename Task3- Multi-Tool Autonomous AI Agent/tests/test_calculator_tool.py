"""
Unit tests for the Safe Calculator Tool.
"""

import unittest
from tools.calculator_tool import CalculatorTool, SafeCalculator


class TestCalculatorTool(unittest.TestCase):
    def setUp(self):
        self.tool = CalculatorTool()

    def test_basic_arithmetic(self):
        self.assertEqual(self.tool.run("4500000 / 32"), "140625")
        self.assertEqual(self.tool.run("1140000 * 0.185"), "210900")
        self.assertEqual(self.tool.run("100 + 250 - 50"), "300")

    def test_percentage_and_currency_sanitization(self):
        self.assertEqual(self.tool.run("$1,000,000 * 15%"), "150000")

    def test_math_functions(self):
        self.assertEqual(self.tool.run("round(sqrt(144) + 8.6)"), "21")
        self.assertEqual(self.tool.run("abs(-42) + min(10, 20)"), "52")

    def test_malicious_code_blocked(self):
        # Attempt to run harmful Python code
        res1 = self.tool.run("__import__('os').system('dir')")
        self.assertIn("Error evaluating expression", res1)

        res2 = self.tool.run("exec('x = 1')")
        self.assertIn("Error evaluating expression", res2)


if __name__ == "__main__":
    unittest.main()
