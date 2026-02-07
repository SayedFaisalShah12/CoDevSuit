import ast
from typing import List, Dict, Any

class CodeSmellDetector(ast.NodeVisitor):
    """
    Detects common code smells in Python code using AST.
    """
    def __init__(self):
        self.smells: List[Dict[str, Any]] = []
        self.current_function = None
        self.depth = 0
        self.MAX_NESTING = 3
        self.MAX_METHOD_LENGTH = 50
        self.MAX_ARGS = 5

    def check(self, tree: ast.AST) -> List[Dict[str, Any]]:
        self.smells = []
        self.visit(tree)
        return self.smells

    def visit_FunctionDef(self, node: ast.FunctionDef):
        # Check argument count
        arg_count = len(node.args.args)
        if arg_count > self.MAX_ARGS:
            self.smells.append({
                "type": "Too Many Arguments",
                "name": node.name,
                "line": node.lineno,
                "details": f"Function has {arg_count} arguments (limit: {self.MAX_ARGS})"
            })

        # Check method length
        length = node.end_lineno - node.lineno
        if length > self.MAX_METHOD_LENGTH:
            self.smells.append({
                "type": "Long Method",
                "name": node.name,
                "line": node.lineno,
                "details": f"Method is {length} lines long (limit: {self.MAX_METHOD_LENGTH})"
            })

        # Track nesting
        old_function = self.current_function
        self.current_function = node.name
        self.generic_visit(node)
        self.current_function = old_function

    def visit_If(self, node: ast.If):
        self.depth += 1
        if self.depth > self.MAX_NESTING:
            self.smells.append({
                "type": "Deeply Nested Code",
                "line": node.lineno,
                "details": f"Nesting depth: {self.depth} (limit: {self.MAX_NESTING})"
            })
        self.generic_visit(node)
        self.depth -= 1

    def visit_While(self, node: ast.While):
        self.depth += 1
        self.generic_visit(node)
        self.depth -= 1

    def visit_For(self, node: ast.For):
        self.depth += 1
        self.generic_visit(node)
        self.depth -= 1
