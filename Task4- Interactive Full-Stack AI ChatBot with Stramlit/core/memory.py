"""
Conversation Memory & Session State Management for the Streamlit Chatbot.
"""

import json
from datetime import datetime
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Optional


@dataclass
class ChatMessage:
    role: str  # "user", "assistant", or "system"
    content: str
    timestamp: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class ConversationMemory:
    """Manages chat message history and session state serialization."""

    def __init__(self, max_history_turns: int = 20):
        self.messages: List[ChatMessage] = []
        self.max_history_turns = max_history_turns

    def add_user_message(self, content: str) -> ChatMessage:
        msg = ChatMessage(role="user", content=content)
        self.messages.append(msg)
        self._trim_history()
        return msg

    def add_assistant_message(self, content: str, metadata: Optional[Dict[str, Any]] = None) -> ChatMessage:
        msg = ChatMessage(role="assistant", content=content, metadata=metadata or {})
        self.messages.append(msg)
        self._trim_history()
        return msg

    def clear(self):
        """Clears all conversation messages."""
        self.messages.clear()

    def _trim_history(self):
        """Maintains memory within the sliding window threshold."""
        max_msgs = self.max_history_turns * 2
        if len(self.messages) > max_msgs:
            self.messages = self.messages[-max_msgs:]

    def export_json(self) -> str:
        """Serializes message history to formatted JSON string."""
        data = [m.to_dict() for m in self.messages]
        return json.dumps(data, indent=2)

    def export_markdown(self) -> str:
        """Exports conversation history to human-readable Markdown format."""
        lines = ["# Datheon AI Chatbot - Conversation Export", ""]
        for m in self.messages:
            speaker = "**User**" if m.role == "user" else "**Datheon AI Assistant**"
            lines.append(f"### {speaker} *({m.timestamp})*")
            lines.append(m.content)
            if m.metadata and "citations" in m.metadata:
                lines.append("\n*Citations:*")
                for cit in m.metadata["citations"]:
                    lines.append(f"- {cit.get('source_file')} (Page {cit.get('page_number')})")
            lines.append("\n---")
        return "\n".join(lines)
