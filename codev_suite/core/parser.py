import ast
from typing import Any, Dict, Optional

class CodeParser:
    """
    Handles parsing of Python source code into AST.
    """
    def __init__(self, source_code: Optional[str] = None, file_path: Optional[str] = None):
        self.source_code = source_code
        self.file_path = file_path
        self.tree: Optional[ast.AST] = None

    def parse(self) -> ast.AST:
        """
        Parses the source code or file content into an AST.
        """
        if self.file_path:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                self.source_code = f.read()
        
        if self.source_code is None:
            raise ValueError("No source code or file path provided.")

        self.tree = ast.parse(self.source_code)
        return self.tree

    def get_structure(self) -> Dict[str, Any]:
        """
        Returns a simplified structure of the code (classes, functions).
        """
        if not self.tree:
            self.parse()
        
        structure = {
            "classes": [],
            "functions": [],
            "imports": []
        }

        for node in ast.walk(self.tree):
            if isinstance(node, ast.ClassDef):
                structure["classes"].append({
                    "name": node.name,
                    "line": node.lineno,
                    "methods": [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
                })
            elif isinstance(node, ast.FunctionDef):
                # Check if it's a top-level function
                if not any(isinstance(parent, ast.ClassDef) for parent in self._get_parents(node)):
                    structure["functions"].append({
                        "name": node.name,
                        "line": node.lineno
                    })
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        structure["imports"].append(alias.name)
                else:
                    structure["imports"].append(node.module)

        return structure

    def _get_parents(self, target_node: ast.AST):
        """
        Helper to find parents of a node. 
        Note: This is a simplified approach; ast.walk doesn't provide parents naturally.
        """
        parents = []
        for node in ast.walk(self.tree):
            for child in ast.iter_child_nodes(node):
                if child == target_node:
                    parents.append(node)
                    parents.extend(self._get_parents(node))
        return parents
