"""
Integration tests for the Multi-Tool Autonomous Agent reasoning loop.
"""

import unittest
from agent.agent_executor import MultiToolAutonomousAgent


class TestAgentExecutor(unittest.TestCase):
    def setUp(self):
        self.agent = MultiToolAutonomousAgent(llm_provider="local")

    def test_compound_budget_and_calculation_query(self):
        query = "Find the 2025 engineering budget in enterprise_budget_2025.json and calculate the allocated budget per engineer."
        result = self.agent.run(query, verbose=False)

        self.assertIsNotNone(result.final_answer)
        self.assertTrue(result.iterations >= 2)
        # Should contain the calculated result 140,625
        self.assertIn("140,625", result.final_answer)

    def test_compound_cloud_savings_query(self):
        query = "Calculate annual cloud savings for 18.5% spot reduction on cloud_cost_breakdown.txt."
        result = self.agent.run(query, verbose=False)

        self.assertIsNotNone(result.final_answer)
        self.assertTrue(result.iterations >= 2)
        # 1140000 * 0.185 = 210,900
        self.assertIn("210,900", result.final_answer)


if __name__ == "__main__":
    unittest.main()
