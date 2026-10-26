"""
Safe Mathematical Calculator Tool for LangChain.
Evaluates arithmetic expressions safely using Python's ast module without using eval().
"""

import ast
import operator
from typing import Union
from pydantic import BaseModel, Field
from langchain_core.tools import tool

# Supported safe operators
SAFE_OPERATORS = {
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


def _safe_eval(node: ast.AST) -> Union[int, float]:
    """Recursively evaluates an AST node containing only arithmetic operations."""
    if isinstance(node, ast.Expression):
        return _safe_eval(node.body)
    elif isinstance(node, ast.Constant):  # Numbers in Python 3.8+
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")
    elif isinstance(node, ast.BinOp):
        op_type = type(node.op)
        if op_type not in SAFE_OPERATORS:
            raise ValueError(f"Unsupported operator: {op_type.__name__}")
        left = _safe_eval(node.left)
        right = _safe_eval(node.right)
        if op_type == ast.Div and right == 0:
            raise ZeroDivisionError("Division by zero is not permitted.")
        return SAFE_OPERATORS[op_type](left, right)
    elif isinstance(node, ast.UnaryOp):
        op_type = type(node.op)
        if op_type not in SAFE_OPERATORS:
            raise ValueError(f"Unsupported unary operator: {op_type.__name__}")
        operand = _safe_eval(node.operand)
        return SAFE_OPERATORS[op_type](operand)
    else:
        raise ValueError(f"Unsupported expression syntax: {type(node).__name__}")


class CalculatorInput(BaseModel):
    expression: str = Field(
        description="The mathematical expression to evaluate, e.g., '25 * 4' or '(100 - 20) / 4'"
    )


@tool("calculator", args_schema=CalculatorInput)
def calculate(expression: str) -> str:
    """
    Safely calculates the result of a mathematical expression.
    Supports addition (+), subtraction (-), multiplication (*), division (/), modulo (%), and powers (**).
    Does NOT use eval() to ensure full execution security.
    """
    try:
        clean_expr = expression.strip()
        # Parse expression into an AST tree
        parsed = ast.parse(clean_expr, mode="eval")
        result = _safe_eval(parsed)
        return f"Result: {result}"
    except ZeroDivisionError:
        return "Error: Division by zero is undefined."
    except Exception as e:
        return f"Calculation error: {str(e)}. Please provide a valid arithmetic expression."
