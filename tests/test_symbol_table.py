import pytest
from symbol_table import SymbolTable

def test_scope_declaration():
    st = SymbolTable()
    sym = st.declare_variable("x", "int", "local")
    assert sym is not None
    assert st.lookup_variable("x") == sym

def test_duplicate_declaration():
    st = SymbolTable()
    st.declare_variable("x", "int", "local")
    assert st.declare_variable("x", "int", "local") is None