from codev_suite.core.parser import CodeParser
import ast

def test_parser_structure():
    code = "class MyClass:\n    def my_method(self):\n        pass\n\ndef my_func():\n    pass"
    parser = CodeParser(source_code=code)
    structure = parser.get_structure()
    
    assert len(structure["classes"]) == 1
    assert structure["classes"][0]["name"] == "MyClass"
    assert "my_method" in structure["classes"][0]["methods"]
    assert len(structure["functions"]) == 1
    assert structure["functions"][0]["name"] == "my_func"

def test_imports():
    code = "import os\nfrom datetime import datetime"
    parser = CodeParser(source_code=code)
    structure = parser.get_structure()
    
    assert "os" in structure["imports"]
    assert "datetime" in structure["imports"]
