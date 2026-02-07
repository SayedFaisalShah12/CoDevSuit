# CoDevSuite Architectural Overview

CoDevSuite is built with modularity and extensibility in mind.

## Core Modules

### 1. `codev_suite.core.parser`
Responsible for converting source code into a structured representation (AST). Currently supports Python using the `ast` module.
**To add new languages:**
- Create a new parser class (e.g., `JSParser`).
- Integrate a language-specific AST library (e.g., `pyjsparser` or `esprima`).

### 2. `codev_suite.analyzers`
Contains logic for different types of analysis.
- `metrics.py`: Quantitative analysis (complexity, length).
- `smells.py`: Pattern-based anti-pattern detection.
- `bugs.py`: Rule-based potential bug identification.
**To add new analyzers:**
- Create a new file in `analyzers/`.
- Inherit from `ast.NodeVisitor` (for Python) or implement a common interface.

### 3. `codev_suite.ai`
Handles high-level semantic analysis using LLMs.
- Currently uses Google Gemini Pro.
- Uses prompt engineering to translate AST/Metric findings into human-readable advice.

### 4. `codev_suite.visualization`
Generates visual representations of metrics and dependencies.
- `graphs.py`: Uses `networkx` for dependency mapping.
- `metrics_viz.py`: Uses `matplotlib` for charts.

## Implementation Details

### Detection Rules for Smells
- **Too Many Arguments**: Functions with > 5 arguments.
- **Long Methods**: Methods > 50 lines.
- **Deep Nesting**: Code blocks nested > 3 levels deep.

### Bug Detection Rules
- **Bare Except**: `except:` blocks without specific types.
- **Boolean Comparison**: `if x == True`.
- **Unreachable Code**: Statements following a `return` or `raise`.

## Future Extensibility
To support multiple languages, the `CodeParser` could be abstracted into a base class with language-specific implementations. The CLI and Web interfaces are already built to handle generic metric objects.
