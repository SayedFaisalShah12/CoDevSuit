# CoDevSuite 🚀

CoDevSuite is an AI-powered developer productivity tool that analyzes Python codebases to reduce complexity and improve code quality.

## Features
- **AST-Based Analysis**: Deep understanding of code structure.
- **Complexity Metrics**: Cyclomatic Complexity, Maintainability Index, and Halstead Metrics.
- **Code Smell Detection**: Identifies long methods, deep nesting, and other anti-patterns.
- **Bug Detection**: Detects bare exceptions, unreachable code, and more.
- **AI-Powered Insights**: Get plain English explanations and refactoring suggestions using Gemini AI.
- **Dependency Graphs**: Visualize your project's architecture.

## Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/CoDevSuite.git
cd CoDevSuite

# Install dependencies
pip install -r requirements.txt
pip install -e .
```

## Usage
### Analyze a File
```bash
codev analyze path/to/file.py
```

### Analyze with AI Insights
```bash
# Set your Gemini API Key
export GEMINI_API_KEY="your_api_key"

codev analyze path/to/file.py --ai
```

### Generate Dependency Graph
```bash
codev graph path/to/directory
```

## Project Structure
- `codev_suite/core`: Core parsing logic.
- `codev_suite/analyzers`: Static analysis (metrics, smells, bugs).
- `codev_suite/ai`: AI integration.
- `codev_suite/visualization`: Graphing and VIS components.
- `codev_suite/cli`: Command-line interface.

## License
MIT
