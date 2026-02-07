import networkx as nx
import matplotlib.pyplot as plt
import ast
import os

class DependencyGraphGenerator:
    """
    Generates dependency graphs based on imports and function calls.
    """
    def __init__(self, directory_path: str):
        self.directory_path = directory_path
        self.graph = nx.DiGraph()

    def build_graph(self):
        """
        Walks through the directory and identifies dependencies.
        """
        for root, _, files in os.walk(self.directory_path):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, self.directory_path)
                    self._analyze_file(file_path, rel_path)

    def _analyze_file(self, file_path, rel_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                tree = ast.parse(f.read())
                self.graph.add_node(rel_path)
                
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            self.graph.add_edge(rel_path, alias.name)
                    elif isinstance(node, ast.ImportFrom):
                        self.graph.add_edge(rel_path, node.module)
            except Exception:
                pass # Skip files that fail to parse

    def visualize(self, output_path: str = "dependency_graph.png"):
        """
        Saves the graph as an image.
        """
        plt.figure(figsize=(12, 8))
        pos = nx.spring_layout(self.graph)
        nx.draw(self.graph, pos, with_labels=True, node_color='lightblue', 
                edge_color='gray', node_size=2000, font_size=10, arrows=True)
        plt.title("Code Dependency Graph")
        plt.savefig(output_path)
        plt.close()
        return output_path
