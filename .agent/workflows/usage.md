---
description: how to use CoDevSuite for analysis and visualization
---

# CoDevSuite Usage Workflow

Follow these steps to analyze your code and generate insights.

## 1. Setup Environment
Ensure dependencies are installed:
```bash
pip install -r requirements.txt
pip install -e .
```

## 2. Basic Static Analysis
Analyze a single file for complexity, smells, and bugs:
// turbo
```bash
python -m codev_suite.cli.main analyze examples/sample_code.py
```

## 3. Architecture Visualization
Generate a dependency graph for the entire project:
// turbo
```bash
python -m codev_suite.cli.main graph codev_suite/
```

## 4. AI-Powered Insights (Optional)
If you have a Gemini API key:
```bash
# Windows
$env:GEMINI_API_KEY="your_api_key_here"
# Linux/Mac
export GEMINI_API_KEY="your_api_key_here"

python -m codev_suite.cli.main analyze examples/sample_code.py --ai
```

## 5. Launch Web Interface
For a premium visual dashboard:
// turbo
```bash
streamlit run codev_suite/web/app.py
```
