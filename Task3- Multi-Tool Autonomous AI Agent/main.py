"""
Multi-Tool Autonomous AI Agent - CLI & Executable Console Runner.

Usage Examples:
  python main.py --demo
  python main.py --query "Read enterprise_budget_2025.json and calculate the budget per engineer."
  python main.py --interactive
"""

import os
import sys
import argparse

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agent.agent_executor import MultiToolAutonomousAgent


def print_banner():
    banner = """
========================================================================
    MULTI-TOOL AUTONOMOUS AI AGENT (ReAct Reasoning Engine)
    Web Search (DuckDuckGo) | Safe Math Calculator | Local File Reader
========================================================================
"""
    print(banner)


def run_demo(provider: str = None):
    """Executes multi-step compound research queries demonstrating autonomous tool orchestration."""
    agent = MultiToolAutonomousAgent(llm_provider=provider)

    demo_queries = [
        "Find the 2025 engineering budget in enterprise_budget_2025.json and calculate the allocated budget per engineer based on headcount.",
        "Look up our annual cloud spend in cloud_cost_breakdown.txt and calculate how much money Datheon saves if we implement the recommended 18.5% spot instance reduction.",
        "Search the web for Datheon AI Technologies and summarize their core specialization.",
    ]

    for idx, q in enumerate(demo_queries, 1):
        print("\n" + "=" * 70)
        print(f"  COMPOUND RESEARCH QUERY {idx}: {q}")
        print("=" * 70)

        result = agent.run(q, verbose=True)
        result.print_trace()

    print("[SUCCESS] Multi-tool autonomous agent demonstration completed successfully!")


def run_interactive(agent: MultiToolAutonomousAgent):
    """Interactive console REPL session for the autonomous agent."""
    print("\n[*] Entering Interactive Autonomous Agent Mode. Type 'exit' or 'quit' to stop.\n")

    while True:
        try:
            query = input("Agent Prompt > ").strip()
            if not query:
                continue
            if query.lower() in ("exit", "quit", "q"):
                print("[*] Exiting Multi-Tool Agent. Goodbye!")
                break

            result = agent.run(query, verbose=True)
            result.print_trace()

        except (KeyboardInterrupt, EOFError):
            print("\n[*] Exiting.")
            break


def main():
    print_banner()

    parser = argparse.ArgumentParser(
        description="Multi-Tool Autonomous AI Agent with ReAct Reasoning Loop."
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run automated compound query demonstration across tools",
    )
    parser.add_argument(
        "--query",
        type=str,
        help="Custom multi-step query for the agent to solve",
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Start interactive console agent session",
    )
    parser.add_argument(
        "--provider",
        choices=["gemini", "openai", "local"],
        default=None,
        help="LLM provider override ('gemini', 'openai', or 'local')",
    )

    args = parser.parse_args()

    agent = MultiToolAutonomousAgent(llm_provider=args.provider)

    if args.query:
        result = agent.run(args.query, verbose=True)
        result.print_trace()
    elif args.interactive:
        run_interactive(agent)
    else:
        run_demo(provider=args.provider)


if __name__ == "__main__":
    main()
