"""
Autonomous Agent Executor implementing the ReAct (Reasoning + Acting) loop.
Displays real-time step-by-step reasoning: Thought -> Action -> Action Input -> Observation -> Final Answer.
"""

import re
import logging
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from langchain_core.tools import BaseTool

from agent.react_prompts import REACT_SYSTEM_PROMPT, format_tools_description
from agent.llm_connector import AgentLLM
from tools.web_search_tool import WebSearchTool
from tools.calculator_tool import CalculatorTool
from tools.file_reader_tool import FileReaderTool

logger = logging.getLogger("AgentExecutor")


@dataclass
class AgentStep:
    thought: str
    action: Optional[str] = None
    action_input: Optional[str] = None
    observation: Optional[str] = None


@dataclass
class AgentResult:
    question: str
    steps: List[AgentStep]
    final_answer: str
    iterations: int

    def print_trace(self):
        """Prints formatted console trace of the agent's full reasoning chain."""
        print("\n" + "=" * 65)
        print(f"  AUTONOMOUS AGENT REASONING TRACE")
        print("=" * 65)
        print(f"Query: {self.question}\n")

        for idx, step in enumerate(self.steps, 1):
            print(f"--- [Step {idx}] ---")
            if step.thought:
                print(f"Thought: {step.thought}")
            if step.action:
                print(f"Action: {step.action}")
                print(f"Action Input: {step.action_input}")
            if step.observation:
                obs_preview = step.observation if len(step.observation) < 300 else step.observation[:300] + "..."
                print(f"Observation:\n{obs_preview}\n")

        print("=" * 65)
        print(f"FINAL ANSWER:\n{self.final_answer}")
        print("=" * 65 + "\n")


class MultiToolAutonomousAgent:
    """Console AI Agent capable of autonomously choosing and invoking tools to solve compound queries."""

    def __init__(
        self,
        tools: Optional[List[BaseTool]] = None,
        llm_provider: Optional[str] = None,
        max_iterations: int = 6,
    ):
        self.tools_list = tools or [WebSearchTool(), CalculatorTool(), FileReaderTool()]
        self.tools_map: Dict[str, BaseTool] = {t.name: t for t in self.tools_list}
        self.llm = AgentLLM(provider=llm_provider)
        self.max_iterations = max_iterations

    def run(self, question: str, verbose: bool = True) -> AgentResult:
        """Executes the autonomous reasoning loop for a given query."""
        tools_desc = format_tools_description(self.tools_list)
        tool_names = ", ".join(self.tools_map.keys())

        system_prompt = REACT_SYSTEM_PROMPT.format(
            tools_description=tools_desc,
            tool_names=tool_names,
        )

        scratchpad = f"{system_prompt}\n\nQuestion: {question.strip()}\n"
        steps: List[AgentStep] = []
        final_answer = ""

        if verbose:
            print(f"\n[*] Starting Multi-Tool Agent Loop for: '{question}'")
            print(f"[*] Available Tools: [{tool_names}]")

        for i in range(1, self.max_iterations + 1):
            if verbose:
                print(f"\n[Iteration {i}/{self.max_iterations}] Thinking...")

            # Generate next step from LLM
            response = self.llm.complete(scratchpad, stop=["\nObservation:"])

            # Check for Final Answer
            if "Final Answer:" in response:
                thought_part = ""
                if "Thought:" in response:
                    thought_match = re.search(r"Thought:\s*(.*?)(?=Final Answer:|$)", response, re.DOTALL)
                    if thought_match:
                        thought_part = thought_match.group(1).strip()

                fa_match = re.search(r"Final Answer:\s*(.*)", response, re.DOTALL)
                final_answer = fa_match.group(1).strip() if fa_match else response.split("Final Answer:")[-1].strip()

                steps.append(AgentStep(thought=thought_part, action=None, action_input=None, observation=None))
                if verbose:
                    if thought_part:
                        print(f"Thought: {thought_part}")
                    print(f"Final Answer: {final_answer}")
                break

            # Parse Thought, Action, and Action Input
            thought_match = re.search(r"Thought:\s*(.*?)(?=Action:|$)", response, re.DOTALL)
            thought = thought_match.group(1).strip() if thought_match else ""

            action_match = re.search(r"Action:\s*([a-zA-Z0-9_\-]+)", response)
            action = action_match.group(1).strip() if action_match else None

            action_input_match = re.search(r"Action Input:\s*(.*?)(?=\nThought:|\nAction:|$)", response, re.DOTALL)
            action_input = action_input_match.group(1).strip() if action_input_match else ""

            if verbose:
                if thought:
                    print(f"Thought: {thought}")
                print(f"Action: {action}")
                print(f"Action Input: {action_input}")

            # Execute tool if valid
            observation = ""
            if action and action in self.tools_map:
                try:
                    tool = self.tools_map[action]
                    observation = tool.run(action_input)
                except Exception as e:
                    observation = f"Error executing tool '{action}': {str(e)}"
            elif action:
                observation = f"Error: Unknown tool '{action}'. Choose from [{tool_names}]."
            else:
                observation = "Error: Could not parse Action. Please output 'Action: <tool_name>' followed by 'Action Input: <input>'."

            if verbose:
                obs_disp = observation if len(observation) < 250 else observation[:250] + "..."
                print(f"Observation: {obs_disp}")

            steps.append(AgentStep(thought=thought, action=action, action_input=action_input, observation=observation))

            # Update scratchpad for next iteration
            scratchpad += f"{response.strip()}\nObservation: {observation.strip()}\n"

        if not final_answer:
            final_answer = "Agent reached maximum iterations without reaching a definitive Final Answer."

        return AgentResult(
            question=question,
            steps=steps,
            final_answer=final_answer,
            iterations=len(steps),
        )
