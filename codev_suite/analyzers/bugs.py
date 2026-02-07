import ast
from typing import List, Dict, Any

class BugDetector(ast.NodeVisitor):
    """
    Identifies potential bugs and dangerous patterns in Python code.
    """
    def __init__(self):
        self.bugs: List[Dict[str, Any]] = []

    def check(self, tree: ast.AST) -> List[Dict[str, Any]]:
        self.bugs = []
        self.visit(tree)
        return self.bugs

    def visit_ExceptHandler(self, node: ast.ExceptHandler):
        if node.type is None:
            self.bugs.append({
                "type": "Bare Except",
                "line": node.lineno,
                "details": "Using 'except:' without specifying an exception class is dangerous."
            })
        self.generic_visit(node)

    def visit_Compare(self, node: ast.Compare):
        # Check for 'if x == True' or 'if x == False'
        for op, right in zip(node.ops, node.comparators):
            if isinstance(op, (ast.Eq, ast.NotEq)):
                if isinstance(right, ast.Constant) and isinstance(right.value, bool):
                    self.bugs.append({
                        "type": "Boolean Comparison",
                        "line": node.lineno,
                        "details": f"Compare using 'if x:' or 'if not x:' instead of '== {right.value}'."
                    })
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef):
        # Check for unreachable code after return
        returned = False
        for body_node in node.body:
            if returned:
                self.bugs.append({
                    "type": "Unreachable Code",
                    "line": body_node.lineno,
                    "details": "Statements after 'return' or 'raise' will never execute."
                })
                break
            if isinstance(body_node, (ast.Return, ast.Raise)):
                returned = True
        self.generic_visit(node)
