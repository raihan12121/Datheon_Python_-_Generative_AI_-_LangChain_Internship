"""
Unit tests for RAG and Agent integration bridges.
"""

import unittest
from core.rag_bridge import RAGBridge
from core.agent_bridge import AgentBridge


class TestBridges(unittest.TestCase):
    def test_rag_bridge_response_and_citations(self):
        bridge = RAGBridge(provider="local")
        answer, citations = bridge.answer("What is the mandatory retention period for inference metadata?")

        self.assertIsNotNone(answer)
        self.assertTrue(len(citations) > 0)
        self.assertEqual(citations[0]["page_number"], 1)

    def test_agent_bridge_execution_and_steps(self):
        bridge = AgentBridge(provider="local")
        answer, steps = bridge.execute_query("Find 2025 engineering budget in enterprise_budget_2025.json and calculate per engineer.")

        self.assertIsNotNone(answer)
        self.assertTrue(len(steps) >= 2)
        self.assertIn("140,625", answer)


if __name__ == "__main__":
    unittest.main()
