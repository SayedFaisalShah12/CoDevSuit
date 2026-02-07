import streamlit as st
import os
import tempfile
from ..core.parser import CodeParser
from ..analyzers.metrics import MetricsAnalyzer
from ..analyzers.smells import CodeSmellDetector
from ..analyzers.bugs import BugDetector
from ..ai.engine import AIEngine
from ..visualization.metrics_viz import MetricsVisualizer
from ..visualization.graphs import DependencyGraphGenerator

st.set_page_config(page_title="CoDevSuite - AI Code Intelligence", layout="wide")

st.title("🚀 CoDevSuite: AI-Powered Code Intelligence")
st.markdown("""
Analyze your Python code for complexity, smells, and bugs. 
Get AI-powered refactoring suggestions and architecture visualizations.
""")

uploaded_file = st.file_uploader("Upload a Python file", type=["py"])

if uploaded_file is not None:
    content = uploaded_file.getvalue().decode("utf-8")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Source Code")
        st.code(content, language="python")
        
    # Analysis
    parser = CodeParser(source_code=content)
    metrics_analyzer = MetricsAnalyzer(content)
    complexity = metrics_analyzer.analyze_complexity()
    mi_score = metrics_analyzer.analyze_maintainability()
    
    detector = CodeSmellDetector()
    smells = detector.check(parser.tree)
    
    bug_detector = BugDetector()
    bugs = bug_detector.check(parser.tree)
    
    with col2:
        st.subheader("Complexity Metrics")
        st.metric("Maintainability Index", f"{mi_score:.2f}")
        
        # Viz
        viz = MetricsVisualizer()
        dist_path = viz.plot_complexity_distribution(complexity)
        st.image(dist_path)
        
        gauge_path = viz.plot_maintainability_gauge(mi_score)
        st.image(gauge_path)

    st.divider()
    
    # Smells and Bugs
    c3, c4 = st.columns(2)
    with c3:
        st.subheader("⚠️ Code Smells")
        if smells:
            for s in smells:
                st.warning(f"**{s['type']}** (Line {s['line']}): {s['details']}")
        else:
            st.success("No code smells detected!")
            
    with c4:
        st.subheader("🐞 Potential Bugs")
        if bugs:
            for b in bugs:
                st.error(f"**{b['type']}** (Line {b['line']}): {b['details']}")
        else:
            st.success("No potential bugs detected!")

    st.divider()
    
    # AI Insights
    st.subheader("🤖 AI Insights")
    if st.button("Get AI Explanation & Refactoring"):
        with st.spinner("Calling Gemini API..."):
            engine = AIEngine()
            explanation = engine.explain_code(content)
            st.info(explanation)
            
            if smells or bugs:
                refactor = engine.suggest_refactor(content, smells + bugs)
                st.success(refactor)
                
    st.divider()
    
    st.subheader("🕸️ Dependency Graph")
    if st.button("Generate Dependency Graph"):
        with tempfile.TemporaryDirectory() as tmpdir:
            # Save the uploaded file to the tmp dir to analyze its imports
            with open(os.path.join(tmpdir, "uploaded_file.py"), "w") as f:
                f.write(content)
            
            generator = DependencyGraphGenerator(tmpdir)
            generator.build_graph()
            graph_path = generator.visualize("web_graph.png")
            st.image(graph_path)
