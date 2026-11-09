"""
Unit tests for the real-time token StreamingEngine.
"""

import unittest
from core.streaming_engine import StreamingEngine


class TestStreamingEngine(unittest.TestCase):
    def setUp(self):
        self.engine = StreamingEngine(provider="local")

    def test_local_streaming_generator(self):
        messages = [{"role": "user", "content": "Tell me about RAG and retention period"}]
        chunks = list(self.engine.stream_chat(messages))

        self.assertTrue(len(chunks) > 5)
        full_text = "".join(chunks)
        self.assertIn("365 days", full_text)
        self.assertIn("PII Masking Gateway", full_text)

    def test_agent_query_streaming(self):
        messages = [{"role": "user", "content": "How do you calculate budget with tools?"}]
        chunks = list(self.engine.stream_chat(messages))

        full_text = "".join(chunks)
        self.assertIn("ReAct", full_text)
        self.assertIn("calculator", full_text)


if __name__ == "__main__":
    unittest.main()
