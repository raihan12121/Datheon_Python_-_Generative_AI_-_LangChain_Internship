"""
Safe Python Math Calculator Tool.
Evaluates mathematical expressions, financial metrics, and statistics using an AST whitelist.
"""

import ast
import math
import operator
from typing import Type
from pydantic import BaseModel, Field
from langchain_core.tools import BaseTool


class CalculatorInput(BaseModel):
    expression: str = Field(..., description="The mathematical expression to evaluate, e.g. '1200000 * 0.185' or '4500000 / 32'.")


class SafeCalculator:
    """Evaluates mathematical AST trees with strict operator and function whitelisting."""

    # Allowed operators
    OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.FloorDiv: operator.floordiv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }

    # Allowed functions
    FUNCTIONS = {
        "abs": abs,
        "round": round,
        "min": min,
        "max": max,
        "sum": sum,
        "sqrt": math.sqrt,
        "ceil": math.ceil,
        "floor": math.floor,
        "log": math.log,
        "exp": math.exp,
    }

    @classmethod
    def evaluate(cls, expr: str) -> float:
        import re
        # Remove currency symbols, percentage to decimal, and commas between digits only
        cleaned = re.sub(r"(?<=\d),(?=\d)", "", expr)
        cleaned = cleaned.replace("$", "").replace("%", "/100").strip()
        parsed = ast.parse(cleaned, mode="eval")
        return cls._eval_node(parsed.body)

    @classmethod
    def _eval_node(cls, node):
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return float(node.value)
            raise ValueError(f"Unsupported constant type: {type(node.value)}")

        elif isinstance(node, ast.BinOp):
            left = cls._eval_node(node.left)
            right = cls._eval_node(node.right)
            op_type = type(node.op)
            if op_type in cls.OPERATORS:
                return cls.OPERATORS[op_type](left, right)
            raise ValueError(f"Unsupported operator: {op_type}")

        elif isinstance(node, ast.UnaryOp):
            operand = cls._eval_node(node.operand)
            op_type = type(node.op)
            if op_type in cls.OPERATORS:
                return cls.OPERATORS[op_type](operand)
            raise ValueError(f"Unsupported unary operator: {op_type}")

        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id in cls.FUNCTIONS:
                args = [cls._eval_node(arg) for arg in node.args]
                return cls.FUNCTIONS[node.func.id](*args)
            raise ValueError(f"Function call not permitted: {ast.dump(node)}")

        raise ValueError(f"Syntax or operation not allowed in calculator: {type(node).__name__}")


class CalculatorTool(BaseTool):
    name: str = "calculator"
    description: str = (
        "Useful for performing mathematical calculations, arithmetic operations, percentages, "
        "and statistical equations. Input must be a valid mathematical expression string."
    )
    args_schema: Type[BaseModel] = CalculatorInput

    def _run(self, expression: str) -> str:
        try:
            result = SafeCalculator.evaluate(expression)
            # Format cleanly
            if isinstance(result, float) and result.is_integer():
                return str(int(result))
            return f"{result:.4f}".rstrip("0").rstrip(".")
        except Exception as e:
            return f"Error evaluating expression '{expression}': {str(e)}"

    async def _arun(self, expression: str) -> str:
        return self._run(expression)
