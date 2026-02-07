from radon.visitors import ComplexityVisitor
from radon.metrics import h_visit, mi_visit
import ast

class MetricsAnalyzer:
    """
    Analyzes code metrics like Cyclomatic Complexity, Halstead metrics, and Maintainability Index.
    """
    def __init__(self, source_code: str):
        self.source_code = source_code

    def analyze_complexity(self):
        """
        Calculates Cyclomatic Complexity for each block.
        """
        def get_rank(cc):
            if cc <= 5: return 'A'
            elif cc <= 10: return 'B'
            elif cc <= 20: return 'C'
            elif cc <= 30: return 'D'
            elif cc <= 40: return 'E'
            return 'F'

        visitor = ComplexityVisitor.from_code(self.source_code)
        type_map = {'F': 'Function', 'C': 'Class', 'M': 'Method'}
        return [
            {
                "type": type_map.get(getattr(block, 'letter', 'F'), 'Block'),
                "name": block.name,
                "complexity": block.complexity,
                "rank": get_rank(block.complexity),
                "lineno": block.lineno
            }
            for block in visitor.blocks
        ]

    def analyze_halstead(self):
        """
        Calculates Halstead metrics.
        """
        metrics = h_visit(self.source_code)
        # Handle the case where h_visit returns a namedtuple or a list of namedtuples
        # Radon's h_visit returns a HalsteadReport
        return {
            "vocabulary": metrics.total.vocabulary,
            "length": metrics.total.length,
            "volume": metrics.total.volume,
            "difficulty": metrics.total.difficulty,
            "effort": metrics.total.effort
        }

    def analyze_maintainability(self):
        """
        Calculates Maintainability Index.
        """
        mi = mi_visit(self.source_code, multi=False)
        return mi
