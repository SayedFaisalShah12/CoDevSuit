import os
import google.generativeai as genai
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

class AIEngine:
    """
    Handles AI-powered code analysis using Gemini.
    """
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-pro')
        else:
            self.model = None

    def explain_code(self, code_snippet: str) -> str:
        """
        Explains code in plain English.
        """
        if not self.model:
            return "AI model not configured. Please set GEMINI_API_KEY."
        
        prompt = (
            "You are an expert software engineer. Explain the following Python code "
            "in plain, concise developer-friendly English. Focus on WHAT it does and WHY.\n\n"
            f"Code:\n```python\n{code_snippet}\n```"
        )
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error calling AI: {str(e)}"

    def suggest_refactor(self, code_snippet: str, smells: list = None) -> str:
        """
        Suggests refactoring improvements.
        """
        if not self.model:
            return "AI model not configured."

        smells_str = ", ".join([s['type'] for s in smells]) if smells else "general complexity"
        prompt = (
            "You are an expert refactoring coach. Analyze this Python code and suggest "
            "specific improvements to reduce complexity, improve readability, and fix "
            f"detected smells like: {smells_str}.\n\n"
            f"Code:\n```python\n{code_snippet}\n```\n\n"
            "Provide the refactored code and an explanation of the changes."
        )

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error calling AI: {str(e)}"
