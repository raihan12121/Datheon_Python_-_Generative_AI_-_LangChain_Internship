"""
Unit tests for ConversationMemory and ChatMessage models.
"""

import json
import unittest
from core.memory import ConversationMemory, ChatMessage


class TestConversationMemory(unittest.TestCase):
    def setUp(self):
        self.memory = ConversationMemory(max_history_turns=3)

    def test_add_messages_and_count(self):
        self.memory.add_user_message("What is the retention period?")
        self.memory.add_assistant_message("365 days", metadata={"citations": [{"source_file": "doc.pdf", "page_number": 1}]})

        self.assertEqual(len(self.memory.messages), 2)
        self.assertEqual(self.memory.messages[0].role, "user")
        self.assertEqual(self.memory.messages[1].role, "assistant")
        self.assertEqual(self.memory.messages[1].metadata["citations"][0]["page_number"], 1)

    def test_sliding_window_trimming(self):
        # max_history_turns = 3, so max messages = 6
        for i in range(10):
            self.memory.add_user_message(f"User query {i}")
            self.memory.add_assistant_message(f"Assistant response {i}")

        self.assertEqual(len(self.memory.messages), 6)
        self.assertEqual(self.memory.messages[-1].content, "Assistant response 9")

    def test_export_json(self):
        self.memory.add_user_message("Hello")
        self.memory.add_assistant_message("Hi there!")

        exported = self.memory.export_json()
        parsed = json.loads(exported)
        self.assertEqual(len(parsed), 2)
        self.assertEqual(parsed[0]["content"], "Hello")

    def test_export_markdown(self):
        self.memory.add_user_message("Show me the doc")
        self.memory.add_assistant_message("Here is the doc", metadata={"citations": [{"source_file": "policy.pdf", "page_number": 2}]})

        md = self.memory.export_markdown()
        self.assertIn("# Datheon AI Chatbot - Conversation Export", md)
        self.assertIn("policy.pdf", md)
        self.assertIn("Page 2", md)


if __name__ == "__main__":
    unittest.main()
