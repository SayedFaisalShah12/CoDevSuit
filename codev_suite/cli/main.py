import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.syntax import Syntax
from ..core.parser import CodeParser
from ..analyzers.metrics import MetricsAnalyzer
from ..analyzers.smells import CodeSmellDetector
from ..analyzers.bugs import BugDetector
from ..visualization.graphs import DependencyGraphGenerator
from ..ai.engine import AIEngine
import os

console = Console()

@click.group()
def cli():
    """CoDevSuite: AI-Powered Code Analysis Tool."""
    pass

@cli.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.option('--ai', is_flag=True, help="Include AI insights")
def analyze(file_path, ai):
    """Analyze a Python source file."""
    console.print(Panel(f"[bold blue]Analyzing:[/bold blue] {file_path}", expand=False))

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 1. Parsing
        parser = CodeParser(source_code=content)
        structure = parser.get_structure()
        
        # 2. Metrics
        metrics_analyzer = MetricsAnalyzer(content)
        complexity = metrics_analyzer.analyze_complexity()
        ma_index = metrics_analyzer.analyze_maintainability()

        # 3. Smells & Bugs
        detector = CodeSmellDetector()
        smells = detector.check(parser.tree)
        
        bug_detector = BugDetector()
        bugs = bug_detector.check(parser.tree)

        # Output Results
        # Complexity Table
        table = Table(title="Cyclomatic Complexity")
        table.add_column("Type", style="cyan")
        table.add_column("Name", style="magenta")
        table.add_column("Complexity", style="green")
        table.add_column("Rank", style="yellow")

        for item in complexity:
            table.add_row(item['type'], item['name'], str(item['complexity']), item['rank'])
        
        console.print(table)
        console.print(f"[bold]Maintainability Index:[/bold] {ma_index:.2f}")

        # Smells
        if smells:
            console.print("\n[bold red]Detected Code Smells:[/bold red]")
            for smell in smells:
                console.print(f"- [yellow]{smell['type']}[/yellow] at line {smell['line']}: {smell['details']}")
        
        # Bugs
        if bugs:
            console.print("\n[bold dark_orange]Potential Bugs:[/bold dark_orange]")
            for bug in bugs:
                console.print(f"- [red]{bug['type']}[/red] at line {bug['line']}: {bug['details']}")

        if not smells and not bugs:
            console.print("\n[green]No common code smells or bugs detected![/green]")

@cli.command()
@click.argument('dir_path', type=click.Path(exists=True))
@click.option('--out', default='dependency_graph.png', help="Output file path")
def graph(dir_path, out):
    """Generate a dependency graph for a directory."""
    console.print(Panel(f"[bold blue]Generating Dependency Graph for:[/bold blue] {dir_path}", expand=False))
    generator = DependencyGraphGenerator(dir_path)
    generator.build_graph()
    path = generator.visualize(out)
    console.print(f"[green]Graph saved to {path}[/green]")

        # 4. AI Insights
        if ai:
            console.print("\n[bold purple]Requesting AI Insights...[/bold purple]")
            engine = AIEngine()
            explanation = engine.explain_code(content)
            console.print(Panel(explanation, title="AI Explanation", border_style="purple"))
            
            if smells:
                refactor = engine.suggest_refactor(content, smells)
                console.print(Panel(refactor, title="Refactoring Suggestions", border_style="green"))

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")

if __name__ == '__main__':
    cli()
