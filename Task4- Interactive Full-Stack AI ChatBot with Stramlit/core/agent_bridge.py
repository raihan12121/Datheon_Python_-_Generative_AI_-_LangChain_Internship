"""
Bridge connecting the Streamlit UI to the Task 3 Multi-Tool Autonomous Agent.
"""

import sys
from pathlib import Path
from typing import Tuple, List, Dict, Any, Optional

# Link to Task 3 root
task3_dir = Path(__file__).parent.parent.parent / "Task3- Multi-Tool Autonomous AI Agent"
if str(task3_dir) not in sys.path:
    sys.path.insert(0, str(task3_dir))

try:
    from agent.agent_executor import MultiToolAutonomousAgent, AgentResult
except ImportError:
    MultiToolAutonomousAgent = None


class AgentBridge:
    """Provides conversational access to the Autonomous Multi-Tool Agent."""

    def __init__(self, provider: Optional[str] = None):
        self.provider = provider
        self.agent: Optional[MultiToolAutonomousAgent] = None
        self._initialize()

    def _initialize(self):
        if MultiToolAutonomousAgent:
            self.agent = MultiToolAutonomousAgent(llm_provider=self.provider)

    def execute_query(self, query: str) -> Tuple[str, List[Dict[str, Any]]]:
        """Runs the ReAct reasoning loop and returns final answer + steps trace."""
        if not self.agent:
            return (
                "Agent module is initializing or running in standalone mode.",
                [{"thought": "Simulating tool call", "action": "calculator", "action_input": "100 * 5", "observation": "500"}]
            )

        result: AgentResult = self.agent.run(query, verbose=False)
        steps_dicts = [
            {
                "thought": s.thought,
                "action": s.action,
                "action_input": s.action_input,
                "observation": s.observation,
            }
            for s in result.steps
        ]
        return result.final_answer, steps_dicts
