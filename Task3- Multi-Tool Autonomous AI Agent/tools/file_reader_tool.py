"""
Local Workspace File Reader and Directory Inspector Tool.
Allows the agent to read JSON, CSV, TXT, and Markdown files safely.
"""

import os
from pathlib import Path
from typing import Type
from pydantic import BaseModel, Field
from langchain_core.tools import BaseTool


class FileReaderInput(BaseModel):
    file_path: str = Field(..., description="Relative or absolute path to local file to read, or 'list:<dir>' to list files.")


class FileReaderTool(BaseTool):
    name: str = "file_reader"
    description: str = (
        "Useful for reading local workspace files (JSON, CSV, TXT, Markdown) or listing directory contents. "
        "Input must be a relative file path (e.g. 'workspace_data/enterprise_budget_2025.json') "
        "or 'list:<dir_path>' to inspect available files."
    )
    args_schema: Type[BaseModel] = FileReaderInput

    def _run(self, file_path: str) -> str:
        clean_input = file_path.strip().strip('"').strip("'")

        # Handle directory listing request
        if clean_input.lower().startswith("list:") or clean_input.lower().startswith("dir:"):
            target_dir = clean_input.split(":", 1)[1].strip() or "."
            return self._list_dir(target_dir)

        # Resolve path
        path = Path(clean_input)
        if not path.is_absolute():
            # Check relative to task root or workspace_data
            base_dir = Path(__file__).parent.parent
            candidate = base_dir / path
            if candidate.exists():
                path = candidate
            else:
                candidate2 = base_dir / "workspace_data" / path.name
                if candidate2.exists():
                    path = candidate2

        if not path.is_file():
            return f"Error: File not found at '{clean_input}'."

        try:
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()

            if len(content) > 4000:
                return content[:4000] + "\n... [Output truncated to 4000 characters]"
            return content

        except Exception as e:
            return f"Error reading file '{clean_input}': {str(e)}"

    def _list_dir(self, dir_name: str) -> str:
        base_dir = Path(__file__).parent.parent
        target = base_dir / dir_name if not Path(dir_name).is_absolute() else Path(dir_name)

        if not target.is_dir():
            return f"Error: Directory not found at '{dir_name}'."

        entries = []
        for p in sorted(target.iterdir()):
            kind = "[DIR] " if p.is_dir() else "[FILE]"
            entries.append(f"{kind} {p.name} ({p.stat().st_size} bytes)")

        return f"Contents of '{dir_name}':\n" + "\n".join(entries)

    async def _arun(self, file_path: str) -> str:
        return self._run(file_path)
