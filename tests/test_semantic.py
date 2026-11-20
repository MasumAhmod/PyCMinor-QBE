import pytest
from semantic import SemanticAnalyzer, analyze

class DummyProgram:
    def __init__(self):
        self.declarations = []

def test_missing_main():
    res = analyze(DummyProgram())
    assert not res.ok
    assert any(d.code == "E001" for d in res.diagnostics)