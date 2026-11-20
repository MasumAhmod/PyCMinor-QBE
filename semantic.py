#semantic

from dataclasses import dataclass, field
from typing import List, Optional
from symbol_table import SymbolTable, Symbol

@dataclass
class Diagnostic:
    code: str
    severity: str
    file: str
    line: int
    column: int
    message: str

@dataclass
class SemanticResult:
    ok: bool
    symbol_table: SymbolTable
    diagnostics: List[Diagnostic]

class SemanticAnalyzer:
    def __init__(self, file_path: str = "main.cm"):
        self.file_path = file_path
        self.symbol_table = SymbolTable()
        self.diagnostics: List[Diagnostic] = []

    def add_error(self, code: str, line: int, col: int, msg: str):
        self.diagnostics.append(Diagnostic(
            code=code, severity="error", file=self.file_path, line=line, column=col, message=msg
        ))

    def analyze(self, program_ast) -> SemanticResult:
        if hasattr(program_ast, 'declarations'):
            for decl in program_ast.declarations:
                self._visit_decl(decl)

        main_sym = self.symbol_table.global_functions.get("main")
        if not main_sym or not main_sym.is_defined:
            self.add_error("E001", 1, 1, "Missing main function definition")
        elif main_sym.return_type != "int" or len(main_sym.param_types) > 0:
            self.add_error("E002", main_sym.line, main_sym.column, "main must be defined as 'int main(void)'")

        for name, sym in self.symbol_table.global_functions.items():
            if not sym.is_defined:
                self.add_error("E003", sym.line, sym.column, f"Function '{name}' declared but never defined")

        ok = len([d for d in self.diagnostics if d.severity == "error"]) == 0
        return SemanticResult(ok=ok, symbol_table=self.symbol_table, diagnostics=self.diagnostics)

    def _visit_decl(self, decl):
        pass

def analyze(program_ast, file_path: str = "main.cm") -> SemanticResult:
    analyzer = SemanticAnalyzer(file_path=file_path)
    return analyzer.analyze(program_ast)

def dump_symbols(semantic_result: SemanticResult):
    print("--- Symbol Table Dump ---")
    for name, sym in semantic_result.symbol_table.global_functions.items():
        print(f"Function: {name} | Return: {sym.return_type} | Params: {sym.param_types} | Defined: {sym.is_defined}")
